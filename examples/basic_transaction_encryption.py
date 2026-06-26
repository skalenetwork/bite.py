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

'''
BITE Python Library - Example: Basic Transaction Encryption

This example demonstrates how to encrypt a transaction using the BITE protocol.
'''

import asyncio
import logging

from bite import BITE


async def main():
    """Main function to run the example."""
    # Replace with your BITE provider URL
    provider_url = 'https://example.com/jsonrpc'

    # Transaction to encrypt
    transaction = {
        'to': '0x1234567890123456789012345678901234567890',
        'data': '0x1234567890abcdef',
        'gas_limit': 500000
    }

    try:
        # Initialize BITE
        bite = BITE(provider_url)

        # Encrypt the transaction
        logging.info('Original transaction:')
        logging.info('  To: %s', transaction["to"])
        logging.info('  Data: %s', transaction["data"])
        logging.info('')

        encrypted_tx = await bite.encrypt_transaction(transaction)

        logging.info('Encrypted transaction:')
        logging.info('  To: %s', encrypted_tx["to"])
        logging.info('  Data: %s...', encrypted_tx["data"][:66])  # Show first 66 chars
        logging.info('  Gas Limit: %s', encrypted_tx["gas_limit"])
        logging.info('')

        # Get committees info
        committees_info = await bite.get_committees_info()
        logging.info('Number of committees: %d', len(committees_info))
        for i, committee in enumerate(committees_info):
            logging.info('Committee %d:', i)
            logging.info('  Epoch ID: %s', committee["epoch_id"])
            logging.info('  BLS Public Key: %s...', committee["common_bls_public_key"][:32])

    except Exception as error: # pylint: disable=broad-except
        logging.info('Error: %s', error)


if __name__ == '__main__':
    asyncio.run(main())
