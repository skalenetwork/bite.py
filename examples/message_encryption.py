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
BITE Python Library - Example: Message Encryption

This example demonstrates how to encrypt a raw message using the BITE protocol.
"""

import asyncio

from bite import BITE


async def main():
    """Main function to run the example."""
    # Replace with your BITE provider URL
    provider_url = 'https://example.com/jsonrpc'

    # Message to encrypt (hex string)
    message = '0x48656c6c6f20574f524c44'  # "Hello WORLD" in hex

    try:
        # Initialize BITE
        bite = BITE(provider_url)

        # Encrypt the message
        print(f"Original message: {message}")

        encrypted_message = await bite.encrypt_message(message)

        print(f"Encrypted message: {encrypted_message[:66]}...")
        print(f"Encrypted message length: {len(encrypted_message)} characters")

    except Exception as error: # pylint: disable=broad-except
        print(f'Error: {error}')


if __name__ == '__main__':
    asyncio.run(main())
