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
from LbPlatformUtils import requires
from LbPlatformUtils.architectures import ARCH_DEFS, get_supported_archs
from LbPlatformUtils.inspect import architecture


def archs():
    return list(get_supported_archs(ARCH_DEFS[architecture()]))


def required(platform):
    return requires(platform).split("-")[0]
