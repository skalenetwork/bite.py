"""
BITE Python Library - Example: Message Encryption

This example demonstrates how to encrypt a raw message using the BITE protocol.
"""

import asyncio
from bite import BITE


async def main():
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
        
    except Exception as error:
        print(f'Error: {error}')


if __name__ == '__main__':
    asyncio.run(main())
