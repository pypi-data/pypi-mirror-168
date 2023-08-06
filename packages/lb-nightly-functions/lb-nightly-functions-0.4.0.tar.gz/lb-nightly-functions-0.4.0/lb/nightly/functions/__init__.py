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
__version__ = "0.4.0"

import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CMAKE_DIR = os.path.join(os.path.dirname(__file__), "data", "cmake")

from . import build, checkout
