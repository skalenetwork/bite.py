"""
BITE Python Library - Example: Basic Transaction Encryption

This example demonstrates how to encrypt a transaction using the BITE protocol.
"""

import asyncio
from bite import BITE


async def main():
    # Replace with your BITE provider URL
    provider_url = 'https://example.com/jsonrpc'
    
    # Transaction to encrypt
    transaction = {
        'to': '0x1234567890123456789012345678901234567890',
        'data': '0x1234567890abcdef',
        'gas_limit': '0x493e0'  # Optional, defaults to 300000
    }
    
    try:
        # Initialize BITE
        bite = BITE(provider_url)
        
        # Encrypt the transaction
        print("Original transaction:")
        print(f"  To: {transaction['to']}")
        print(f"  Data: {transaction['data']}")
        print()
        
        encrypted_tx = await bite.encrypt_transaction(transaction)
        
        print("Encrypted transaction:")
        print(f"  To: {encrypted_tx['to']}")
        print(f"  Data: {encrypted_tx['data'][:66]}...")  # Show first 66 chars
        print(f"  Gas Limit: {encrypted_tx['gas_limit']}")
        print()
        
        # Get committees info
        committees_info = await bite.get_committees_info()
        print(f"Number of committees: {len(committees_info)}")
        for i, committee in enumerate(committees_info):
            print(f"Committee {i}:")
            print(f"  Epoch ID: {committee['epoch_id']}")
            print(f"  BLS Public Key: {committee['common_bls_public_key'][:32]}...")
        
    except Exception as error:
        print(f'Error: {error}')


if __name__ == '__main__':
    asyncio.run(main())
