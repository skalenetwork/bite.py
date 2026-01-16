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
BITE Python Library - Conftest for pytest
"""

import os
import sys
from unittest.mock import MagicMock

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock skale_te module if not present
try:
    import skale_te
except ImportError:
    skale_te = MagicMock()

    def mock_encrypt(data):
        return f"encrypted_{data}"

    skale_te.encrypt_message.side_effect = mock_encrypt
    skale_te.encrypt_message_dual_key.side_effect = mock_encrypt

    def mock_encrypt_mockup(data):
        return data + "abcdef123456"

    skale_te.encrypt_message_mockup.side_effect = mock_encrypt_mockup

    sys.modules['skale_te'] = skale_te
