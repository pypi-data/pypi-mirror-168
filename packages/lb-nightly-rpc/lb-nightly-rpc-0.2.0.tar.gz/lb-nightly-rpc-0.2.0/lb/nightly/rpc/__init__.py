###############################################################################
# (c) Copyright 2020-2022 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
__version__ = "0.2.0"

import logging
import os
import ssl
from datetime import datetime, timedelta
from urllib.parse import urlsplit

from celery import Celery
from celery.signals import celeryd_after_setup, worker_process_init
from celery.utils.log import get_task_logger
from kombu import Queue
from lb.nightly.configuration import get as lbget
from lb.nightly.configuration import service_config

from . import archs, scheduler, tasks
from ._task_helpers import get_task_priority

conf = service_config(silent=True)
try:
    broker_url = conf.get("rabbitmq", {}).get("url")
    backend_url = conf.get("mysql", {}).get("url")
except AttributeError:
    logging.warning("Broker and Backend not specified, the results will not be kept")
    broker_url = os.environ.get("BROKER_URL", "amqp://guest:guest@rabbitmq:5672")
    backend_url = os.environ.get("BACKEND_URL", "rpc")

app = Celery(
    __name__,
    broker=broker_url,
    backend=backend_url,
)

from .beat import setup_periodic_tasks

if "amqps" in urlsplit(broker_url).scheme or "ssl=true" in urlsplit(broker_url).query:
    app.conf.broker_use_ssl = {
        "cert_reqs": ssl.CERT_REQUIRED,
        "server_hostname": urlsplit(broker_url).hostname,
    }

app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_track_started=True,
    result_extended=True,
    worker_deduplicate_successful_tasks=True,
)

queue_arguments = {
    "x-message-ttl": (conf or {})
    .get("rabbitmq", {})
    .get("x-message-ttl", timedelta(hours=24) // timedelta(milliseconds=1)),
    "x-max-priority": (conf or {}).get("rabbitmq", {}).get("x-max-priority", 100),
}

queues = {
    "checkout": Queue(
        "checkout", routing_key="checkout.#", queue_arguments=queue_arguments
    ),
    "scheduler": Queue(
        "scheduler", routing_key="scheduler.#", queue_arguments=queue_arguments
    ),
    "beat": Queue("beat", routing_key="beat.#", queue_arguments=queue_arguments),
}
for arch in archs.archs():
    queues[f"build-{arch}"] = Queue(
        f"build-{arch}", routing_key=f"build-{arch}.#", queue_arguments=queue_arguments
    )
    queues[f"test-{arch}"] = Queue(
        f"test-{arch}", routing_key=f"test-{arch}.#", queue_arguments=queue_arguments
    )


# global variable to store the path to worker process directory
# the value is set at worker process initialisation
worker_process_dir = ""


@worker_process_init.connect()
def configure_worker(signal=None, sender=None, **kwargs):
    global worker_process_dir
    worker_process_dir = os.path.join(
        os.path.dirname(os.environ["CELERY_LOG_FILE"]),
        os.path.splitext(os.path.basename(os.environ["_MP_FORK_LOGFILE_"]))[0],
    )
    if worker_process_dir:
        os.makedirs(worker_process_dir, exist_ok=True)


@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    # disable default queue named 'celery'
    instance.app.amqp.queues.deselect("celery")
    worker_type = sender.split("@")[0]
    for queue in queues.values():
        if queue.name.split("-")[0] == worker_type:
            instance.app.amqp.queues.select_add(queue)


def route_task(name, args, kwargs, options, task=None, **kw):
    if name == "lb.nightly.rpc.tasks.checkout":
        return {"queue": queues.get("checkout")}
    elif name.startswith("lb.nightly.rpc.scheduler."):
        return {"queue": queues.get("scheduler")}
    elif name.startswith("lb.nightly.rpc.beat."):
        return {"queue": queues.get("beat")}
    elif name.startswith("lb.nightly.rpc.tasks."):
        # build and test tasks require 'platform' arguments which is args[1]
        arch = archs.required(args[1])
        return {"queue": queues.get(f"{name.split('.')[-1]}-{arch}")}


app.conf.task_routes = (route_task,)
app.conf.task_default_exchange = "tasks"
app.conf.task_default_exchange_type = "direct"
app.conf.task_default_priority = 51

logger = get_task_logger(__name__)


_checkout = app.task(tasks.checkout)
_build = app.task(tasks.build)
_test = app.task(tasks.test)


def checkout(*args, **kwargs):
    project = lbget(args[0])
    priority = get_task_priority(slot=project.slot.name, project=project.name)
    return _checkout.apply_async(
        args=args,
        kwargs=kwargs,
        priority=priority,
        expires=datetime.now() + timedelta(days=1),
        retry=True,
        retry_policy={
            "max_retries": 3,
            "interval_start": 1,
            "interval_step": 0.2,
            "interval_max": 0.2,
        },
    ).get()


def build(*args, **kwargs):
    project = lbget(args[0])
    priority = get_task_priority(
        slot=project.slot.name, project=project.name, platform=args[1]
    )
    return _build.apply_async(
        args=args,
        kwargs=kwargs,
        priority=priority,
        expires=datetime.now() + timedelta(days=1),
        retry=True,
        retry_policy={
            "max_retries": 3,
            "interval_start": 1,
            "interval_step": 0.2,
            "interval_max": 0.2,
        },
    ).get()


def test(*args, **kwargs):
    project = lbget(args[0])
    priority = (
        get_task_priority(
            slot=project.slot.name, project=project.name, platform=args[1]
        )
        - 10
    )
    priority = 0 if priority < 0 else priority
    return _test.apply_async(
        args=args,
        kwargs=kwargs,
        priority=priority,
        expires=datetime.now() + timedelta(days=1),
        retry=True,
        retry_policy={
            "max_retries": 1,
            "interval_start": 1,
            "interval_step": 0.2,
            "interval_max": 0.2,
        },
    ).get()


_start_slot = app.task(scheduler.start_slot)


def start_slot(*args, **kwargs):
    priority = get_task_priority(slot=lbget(args[0]).name)
    return _start_slot.apply_async(
        args=args,
        kwargs=kwargs,
        priority=priority,
        expires=datetime.now() + timedelta(days=1),
        retry=True,
        retry_policy={
            "max_retries": 3,
            "interval_start": 1,
            "interval_step": 0.2,
            "interval_max": 0.2,
        },
    ).forget()
