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
BITE Python Library - Helper functions
"""

from typing import Any, Dict
from urllib.parse import urlparse


class CommonPublicKeyResponse:
    """Response object for committee information."""
    # pylint: disable=too-few-public-methods

    def __init__(self, common_bls_public_key: str, epoch_id: int):
        self.common_bls_public_key = common_bls_public_key
        self.epoch_id = epoch_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'common_bls_public_key': self.common_bls_public_key,
            'epoch_id': self.epoch_id
        }


def remove_0x_prefix_if_needed(hex_str: str) -> str:
    """
    Remove '0x' prefix from hex string if present.

    Args:
        hex_str: Hex string with or without '0x' prefix

    Returns:
        Hex string without '0x' prefix
    """
    return hex_str[2:] if hex_str.startswith('0x') else hex_str


def validate_url(url: str) -> None:
    """
    Validate that a string is a valid URL.

    Args:
        url: URL string to validate

    Raises:
        ValueError: If URL is invalid
    """
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValueError(f"Invalid provider URL: {url}")
    except Exception as exc:
        raise ValueError(f"Invalid provider URL: {url}") from exc


def validate_hex_string(hex_str: str) -> None:
    """
    Validate that a string contains only hex characters and has even length.

    Args:
        hex_str: Hex string to validate (without '0x' prefix)

    Raises:
        ValueError: If string is not valid hex or has odd length
    """
    if not all(c in '0123456789abcdefABCDEF' for c in hex_str):
        raise ValueError("Invalid input: Must contain only hexadecimal characters")

    if len(hex_str) % 2 != 0:
        raise ValueError("Invalid input: Must have an even length")
