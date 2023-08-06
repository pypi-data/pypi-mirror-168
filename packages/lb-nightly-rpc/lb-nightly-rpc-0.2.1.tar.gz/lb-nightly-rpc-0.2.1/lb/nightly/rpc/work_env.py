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
from contextlib import contextmanager
from pathlib import Path
from shutil import copyfileobj
from subprocess import CalledProcessError, run
from urllib.request import urlopen

import yaml
from celery.utils.log import get_task_logger

DEFAULT_ENVIRONMENT = {
    "name": "default-nightlies-env",
    "channels": ["conda-forge", "defaults"],
    "dependencies": [
        "python",
        "cmake",
        "ninja",
        "ccache",
        "pip",
        {
            "pip": [
                "git+https://gitlab.cern.ch/lhcb-core/nightly-builds/lb-nightly-functions.git@master"
            ]
        },
    ],
}

logger = get_task_logger(__name__)


class CondaEnv:
    """
    Class creating conda environment
    """

    def __init__(
        self,
        base_dir=os.getcwd(),
        environment=None,
    ):
        self.base_dir = base_dir
        self.environment = environment or DEFAULT_ENVIRONMENT
        self.cvmfs = False
        os.makedirs(f"{self.base_dir}/pkgs", exist_ok=True)
        os.environ["CONDA_PKGS_DIRS"] = f"{self.base_dir}/pkgs"
        self.conda_cmd = Path(
            "/cvmfs/lhcbdev.cern.ch/conda/miniconda/linux-64/prod/bin/conda"
        )
        self.conda_activate = Path(
            "/cvmfs/lhcbdev.cern.ch/conda/miniconda/linux-64/prod/bin/activate"
        )
        logger.debug(f"Using conda from: {self.conda_cmd}")

        try:
            override_env = (
                Path(os.environ["FUNCTIONS_ENV"])
                if os.environ.get("FUNCTIONS_ENV")
                else Path.home() / "override_envs" / "functions"
            )
            self.prefix = (
                override_env
                if override_env.exists()
                else (
                    Path("/cvmfs/lhcbdev.cern.ch/nightly-environments")
                    / self.environment["name"]
                )
            )
            self.bin_dir = self.prefix / "bin"
            self.python = self.bin_dir / "python"
            assert self.prefix.exists()
            assert self.bin_dir.exists()
            assert self.python.exists()
            self.cvmfs = True
            logger.debug(f"Using environment from: {self.prefix}")

        except (KeyError, AssertionError):
            # if the environment does not exist on cvmfs
            # or its name was not specified
            # let's try to create it
            self.prefix = os.path.join(self.base_dir, "nightlies-env")

            # if the environment in slot metadata is missing
            # we take the default one
            # otherwise, let's assume the dictionary is complete
            # and can be directly dumped to environment.yml used
            # to create conda environment

            if not self.conda_cmd.exists():
                self.conda_cmd = Path(self.base_dir) / "miniconda" / "bin" / "conda"
                if not self.conda_cmd.exists():
                    # If conda installation is missing, we need to set it up.
                    logger.debug("Installing conda")
                    with urlopen(
                        "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
                    ) as response:
                        with open(f"{self.base_dir}/miniconda.sh", "wb") as outfile:
                            copyfileobj(response, outfile)
                    init_conda_cmd = [
                        "bash",
                        f"{self.base_dir}/miniconda.sh",
                        "-b",
                        "-u",
                        "-p",
                        f"{self.base_dir}/miniconda",
                    ]
                    try:
                        run(init_conda_cmd, check=True, timeout=1800)
                    except CalledProcessError as err:
                        logger.error("Couldn't setup conda installation")
                        raise EnvironmentError(err.stderr.decode())
                    os.remove(f"{self.base_dir}/miniconda.sh")

            logger.debug(f"Using conda from: {self.conda_cmd}")
            self.env_yml = f"{self.base_dir}/environment.yml"

    @contextmanager
    def __call__(self):
        """
        Calling class object yields context manager
        """

        if not self.cvmfs:
            try:
                # check if there's existing environment.yml
                # and if so, compare with the requested environment
                # no need for creating the new conda env
                # if they're the same
                old_env = {}
                with open(self.env_yml, "r") as old_env_file:
                    old_env = yaml.safe_load(old_env_file)
                assert old_env == self.environment
                # make sure there's at least python executable in the environment
                assert os.path.exists(f"{self.prefix}/bin/python")
                logger.debug("Reusing the existing environment")
            except (FileNotFoundError, AssertionError):
                logger.debug("Creating conda environment")
                with open(self.env_yml, "w") as envfile:
                    envfile.write(yaml.safe_dump(self.environment))
                env_cmd = [
                    self.conda_cmd,
                    "env",
                    "create",
                    "--file",
                    self.env_yml,
                    "--prefix",
                    self.prefix,
                    "--force",
                ]
                try:
                    run(env_cmd, check=True, capture_output=True, timeout=1800)
                except (OSError, CalledProcessError) as err:
                    logger.error("Creating conda environment failed")
                    raise EnvironmentError(err.stderr.decode())

            self.bin_dir = f"{self.prefix}/bin/"
            self.python = f"{self.prefix}/bin/python"

        # make sure lb.nightly.functions package is installed
        cmd = [
            self.python,
            "-c",
            "import lb.nightly.functions",
        ]
        try:
            run(cmd, env={"PATH": self.bin_dir}, check=True, capture_output=True)
        except CalledProcessError as err:
            logger.error("lb.nightly.functions not available in the environment")
            raise EnvironmentError(err.stderr.decode())

        yield self

    def dump_environment(self):
        """
        Return string containing the packages with versions available in this environment
        """
        return run(
            [
                self.conda_cmd,
                "list",
                "--export",
                "-p",
                self.prefix,
            ],
            capture_output=True,
        ).stdout.decode()
