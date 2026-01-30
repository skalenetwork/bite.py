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

import asyncio
import os
import traceback

from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3

from bite.bite import BITE

load_dotenv()


# --- Configuration ---
# Replace these with your actual values or set environment variables
RPC_URL = os.environ.get("RPC_URL", "None")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", "YOUR_PRIVATE_KEY")
RECEIVER_ADDRESS = "0x9373ABadDfaa85B9fA2Bdeb4d4F28b66E00CCf52" # Replace with receiver
DATA_TO_ENCRYPT = "0xa694fc3a000000000000000000000000000000000000000000000000000000000000000d"

async def main():
    # 1. Setup Web3
    if not RPC_URL or RPC_URL == "None":
        print("Error: RPC_URL is not set.")
        return

    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        print(f"Error: Unable to connect to RPC URL: {RPC_URL}")
        return
    print(f"Connected to {RPC_URL}")

    # 2. Setup Account
    if "YOUR_PRIVATE_KEY" in PRIVATE_KEY or not PRIVATE_KEY:
        print("Error: Please set a valid PRIVATE_KEY")
        # For demonstration purposes, we'll stop here if no key is provided
        return

    try:
        account = Account.from_key(PRIVATE_KEY)
        sender_address = account.address
        print(f"Sender Address: {sender_address}")
    except Exception as e:
        print(f"Error loading private key: {e}")
        return

    # 3. Prepare Transaction Data for BITE
    # BITE expects 'to', 'data', and optionally 'gas_limit'
    tx_to_encrypt = {
        'to': RECEIVER_ADDRESS,
        'data': DATA_TO_ENCRYPT,
        'gas_limit': 500000
    }

    # 4. Encrypt Transaction using BITE Core Library
    # The BITE high-level class handles retrieving the key from the endpoint and the encryption
    try:
        print("Initializing BITE client...")
        bite_client = BITE(RPC_URL)

        print("Encrypting transaction...")
        # This calls bite.core.encrypt.encrypt_transaction internally, which is async
        encrypted_result = await bite_client.encrypt_transaction(tx_to_encrypt)

        print("Transaction encrypted successfully.")
        # print(f"encrypted_result: {encrypted_result}")

    except Exception as e:
        print(f"Error during encryption: {e}")
        traceback.print_exc()
        return

    # 5. Build Final Ethereum Transaction
    try:
        nonce = w3.eth.get_transaction_count(sender_address)

        # Parse gas limit from encryption result or use fallback
        gas = int(500000)
        if 'gas_limit' in encrypted_result:
             val = encrypted_result['gas_limit']
             if isinstance(val, str) and val.startswith('0x'):
                 gas = int(val, 16)
             elif isinstance(val, int):
                gas = val
             else:
                 gas = int(val)

        transaction = {
            'to': encrypted_result['to'],
            'data': encrypted_result['data'],
            'value': w3.to_wei(0.01, 'ether'),
            'gas': gas,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': w3.eth.chain_id
        }

        print("Signing transaction...")
        signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

        print("Sending transaction...")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction sent! Hash: {tx_hash.hex()}")

        # 6. Wait for Receipt
        print("Waiting for receipt...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 1:
            print("Transaction successful!")
        else:
            print("Transaction failed!")

    except Exception as e:
        print(f"Error sending transaction: {e}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
