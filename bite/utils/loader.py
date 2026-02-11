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
BITE Python Library - Loader
"""

import ctypes
import os


def preload_dependencies(lib_name: str = 'libcrypto.so.1.1') -> None:
    """
    Preload bundled libraries (e.g. libcrypto) if present.
    This is required for skale_te to find its dependencies when installed as a wheel.

    Args:
        lib_name: Name of the library to preload. Defaults to 'libcrypto.so.1.1'.
    """
    try:
        # Look for bundled library relative to the bite package root
        # This file is in bite/utils/, so we go up one level to bite/
        # and then into lib/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bite_root = os.path.dirname(current_dir)
        bundled_lib = os.path.join(bite_root, 'lib', lib_name)

        if os.path.exists(bundled_lib):
            ctypes.CDLL(bundled_lib, mode=ctypes.RTLD_GLOBAL)
    except OSError:
        pass
