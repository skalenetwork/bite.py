"""
BITE Python Library - Helper functions

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

@copyright SKALE Labs 2025-Present
"""

from urllib.parse import urlparse


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
