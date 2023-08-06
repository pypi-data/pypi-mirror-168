###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import time
from datetime import timedelta

from celery.schedules import crontab
from celery.utils.log import get_task_logger

from . import app

logger = get_task_logger(__name__)


@app.task(bind=True)
def revoke_tasks(timeout=timedelta(hours=24).total_seconds()):
    """Revokes all the tasks running for more than timeout parameter (24h by default)"""
    for _, tasks in app.control.inspect().active().items():
        for task in tasks:
            if time.time() - task["time_start"] > timeout:
                logger.debug(
                    f"Revoking task running longer than {timeout} seconds: {task}"
                )
                app.control.revoke(task["id"], terminate=True)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour="*/3"),
        revoke_tasks.s(timeout=timedelta(hours=24).total_seconds()),
        name="revokes all the tasks running more than 24h",
        expires=timedelta(hours=3).total_seconds(),
    )
