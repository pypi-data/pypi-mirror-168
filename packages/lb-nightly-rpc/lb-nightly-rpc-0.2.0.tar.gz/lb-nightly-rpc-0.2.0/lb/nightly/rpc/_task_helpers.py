###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import logging
import time

import requests
import yaml

# Code below adapted from
# https://gitlab.cern.ch/lhcb-core/tasks/lbtaskweb/-/blob/master/src/lbtaskweb/hooks/build_ready.py

# defaults in case GitLab is down or malformed
nightly_conf_last_update = 0
nightly_conf = {
    "default": {
        "slot": 0.8,
        "project": 0.8,
        "platforms": 0.8,
    },
    "slots": {
        "lhcb-head": 1.0,
        "lhcb-lcg-dev3": 0.8,
        "lhcb-lcg-dev4": 0.8,
        "lhcb-run2-patches": 0.8,
    },
    "projects": {},
    "platforms": {},
    "overrides": {},
}


def nightly_deployment_config() -> dict:
    global nightly_conf
    global nightly_conf_last_update
    # Update at most once per 1 minute
    if nightly_conf_last_update < time.time() - 60:
        try:
            r = requests.get(
                "https://gitlab.cern.ch/lhcb-core/LHCbNightlyConf"
                "/-/raw/master/cvmfs-priorities.yaml",
                timeout=5,
            )
            r.raise_for_status()
            nightly_conf = yaml.safe_load(r.text)
        except Exception:
            logging.warning("Failed to get cvmfs-priorities.yaml from LHCbNightlyConf")
        nightly_conf_last_update = time.time()
    return nightly_conf


def get_task_priority(slot: str, project: str = None, platform: str = None) -> int:
    """
    Calculates the priority of the nightly task by multiplying
    the priority for the slot, project and the platform.
    It uses data from cvmfs-priorities.yaml in LHCbNightlyConf,
    where a float from [0,1] range is assigned to slot, project,
    and platform.

    Returns integer from [0,100] range.

    See also https://gitlab.cern.ch/lhcb-core/LHCbNightlyConf/-/blob/master/cvmfs-priorities.yaml
    """
    nightly_conf = nightly_deployment_config()

    def_slot = nightly_conf["default"]["slot"]
    def_project = nightly_conf["default"]["project"]
    def_platforms = nightly_conf["default"]["platforms"]

    # slot priority in cvmfs-priorities.yaml might be 0 because
    # we don't deploy every slot, so 'or 0.8' protects against that
    slot_priority = nightly_conf.get("slots", {}).get(slot, def_slot) or 0.8
    project_priority = nightly_conf.get("projects", {}).get(project, def_project)
    platform_priority = nightly_conf.get("platforms", {}).get(platform, def_platforms)

    priority = slot_priority * project_priority * platform_priority
    override = nightly_conf["overrides"].get(slot, {}).get(project, {}).get(platform)

    return int(round((override if override else priority) * 100))
