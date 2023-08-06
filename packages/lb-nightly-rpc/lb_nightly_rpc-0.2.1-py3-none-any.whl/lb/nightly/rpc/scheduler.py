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
from subprocess import run


def start_slot(slot):
    """
    Invoke luigi command to start the build of a slot.
    """
    run(
        [
            "luigi",
            "--workers=300",
            "--module=lb.nightly.scheduler.workflow",
            "--log-level=INFO",
            "Slot",
            "--slot",
            slot,
        ]
    )
