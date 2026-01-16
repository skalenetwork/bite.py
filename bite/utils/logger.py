#   -*- coding: utf-8 -*-
#
#   This file is part of SKALE.py
#
#   Copyright (C) 2019-Present SKALE Labs
#
#   SKALE.py is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   SKALE.py is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with SKALE.py.  If not, see <https://www.gnu.org/licenses/>.

"""
BITE Python Library - Logger
"""

import logging
import sys

from .constants import NODE_ENV

# Configure logger
logger = logging.getLogger("bite")

# Set log level based on environment
if NODE_ENV == "development":
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.CRITICAL)

# Create console handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
if not logger.handlers:
    logger.addHandler(handler)

__all__ = ['logger']
