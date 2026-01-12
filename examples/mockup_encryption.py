"""
BITE Python Library - Example: Mockup Encryption for Testing

This example demonstrates how to use the BITEMockup class for testing
without connecting to a real BITE endpoint.
"""

import asyncio
from bite import BITEMockup


async def main():
    # Transaction to encrypt
    transaction = {
        'to': '0x1234567890123456789012345678901234567890',
        'data': '0x1234567890abcdef'
    }
    
    try:
        # Initialize BITE Mockup
        bite_mock = BITEMockup()
        
        # Encrypt the transaction (mock)
        print("Original transaction:")
        print(f"  To: {transaction['to']}")
        print(f"  Data: {transaction['data']}")
        print()
        
        encrypted_tx = await bite_mock.encrypt_transaction(transaction)
        
        print("Mock encrypted transaction:")
        print(f"  To: {encrypted_tx['to']}")
        print(f"  Data: {encrypted_tx['data'][:66]}...")
        print(f"  Gas Limit: {encrypted_tx['gas_limit']}")
        print()
        
        # Encrypt a message (mock)
        message = '0x48656c6c6f20574f524c44'
        print(f"Original message: {message}")
        
        encrypted_message = await bite_mock.encrypt_message(message)
        print(f"Mock encrypted message: {encrypted_message[:66]}...")
        
    except Exception as error:
        print(f'Error: {error}')


if __name__ == '__main__':
    asyncio.run(main())
