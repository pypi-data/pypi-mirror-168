###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import os
from functools import wraps
from subprocess import CalledProcessError, run
from tempfile import TemporaryDirectory

from celery import current_task
from celery.utils.log import get_task_logger
from lb.nightly.configuration import get

from .work_env import CondaEnv

logger = get_task_logger(__name__)


def nightly_task(task):
    @wraps(task)
    def wrapper(project_id, *args, **kwargs):
        logfile = os.path.join(
            os.path.dirname(os.environ["CELERY_LOG_FILE"]),
            f"{task.__name__}_{current_task.request.id}.log",
        )
        os.environ.update({"TASK_LOGFILE": logfile})
        from . import worker_process_dir

        with CondaEnv(
            base_dir=worker_process_dir,
            environment=get(project_id).slot.metadata.get("environment"),
        )() as env:
            with TemporaryDirectory(dir=env.base_dir) as tmpdir:
                cmd = [
                    env.python,
                    "-m",
                    "lb.nightly.functions.rpc",
                    *task(project_id, *args, **kwargs),
                    current_task.request.id,
                ]
                wenv = dict(os.environ)
                if str(env.bin_dir) not in wenv["PATH"]:
                    wenv["PATH"] = f"{env.bin_dir}:{wenv['PATH']}"
                if "CONDA_ENV" not in wenv:
                    wenv[
                        "CONDA_ENV"
                    ] = (
                        env.prefix
                    )  # needed to mount the dir inside singularity container

                try:
                    result = run(
                        cmd, cwd=tmpdir, capture_output=True, check=True, env=wenv
                    )
                except CalledProcessError as err:
                    result = err
                    result.args = result.args[1]
                    raise
                finally:
                    with open(logfile, "a") as logs:
                        logs.write(
                            f"{'='*80}\ncommand: {result.args} exited "
                            f"with returncode: {result.returncode}\n"
                            f"{'='*80}\nstdout:\n{'-'*80}\n{result.stdout.decode()}\n"
                            f"{'='*80}\nstderr:\n{'-'*80}\n{result.stderr.decode()}\n"
                            f"{'='*80}\nenvironment:\n{'-'*80}\n{env.dump_environment()}\n"
                        )

    return wrapper


@nightly_task
def checkout(
    project_id: str,
):
    return (
        "checkout",
        project_id,
    )


@nightly_task
def build(
    project_id: str,
    platform: str,
):
    return (
        "build",
        project_id,
        platform,
    )


@nightly_task
def test(
    project_id: str,
    platform: str,
):
    return (
        "test",
        project_id,
        platform,
    )
