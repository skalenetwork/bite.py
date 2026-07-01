# skale-bite

## Description
`skale-bite` is a Python library for encrypting transaction data using the BITE (Blockchain Integrated Threshold Encryption) protocol. BITE is an extension of the SKALE provably secure consensus protocol that enables threshold encryption of transaction data.

The library provides functionality to:
- Encrypt transaction data using BLS threshold encryption public keys
- Handle both single and dual committee encryption scenarios during committee rotations
- Interact with BITE-enabled SKALE chains via JSON-RPC methods

### How BITE Works
Nodes participating in a SKALE consensus committee share a common threshold encryption (TE) public key and possess a set of TE private key shares. The committee size is typically `3t + 1`, where `t` is an integer. A user can encrypt plaintext using the TE public key. To decrypt the resulting ciphertext, a threshold decryption protocol must be executed by a supermajority of `2t + 1` nodes.

### Committee Rotation Support
During committee rotation periods, the library automatically handles dual encryption:
- **Single Committee**: Normal operation where data is encrypted once with the current committee's BLS public key
- **Dual Committee**: During rotation periods, data is encrypted with both current and next committee keys to ensure seamless transitions

## Installation
Install the library using pip:

```bash
pip install skale-bite
```

## Usage

> ⚠️ **Warning**  
> When passing a transaction to `bite`, it is necessary to set the gas_limit field manually.
> This is because estimateGas does not return a proper value for encrypted transactions.
> Always calculate and set `gas_limit` manually for your specific transaction.

Here is an example of how to use the library to encrypt transaction data:

```python
import asyncio
from bite import BITE

async def main():
    provider_url = 'https://example.com/jsonrpc'  # Replace with your provider URL
    transaction = {
        'to': '0x1234567890123456789012345678901234567890',
        'data': '0x1234567890abcdef'
        'gas_limit': 500000
    }

    try:
        bite = BITE(provider_url)

        # Encrypt transaction using the BLS public key
        encrypted_tx = await bite.encrypt_transaction(transaction)
        print('Encrypted Transaction:', encrypted_tx)

        # Optionally get the committees info
        committees_info = await bite.get_committees_info()
        print('Committees Info:', committees_info)
        print('Current BLS Public Key:', committees_info[0]['common_bls_public_key'])
        print('Current Epoch ID:', committees_info[0]['epoch_id'])
    except Exception as error:
        print('Encryption Error:', error)

asyncio.run(main())
```

## API Reference

---

### `BITE(endpoint: str)`

Creates a new instance of the `BITE` class, configured to use a specific BITE JSON-RPC endpoint.

- **Parameters**:
  - `endpoint`: `str` – The BITE URL provider (JSON-RPC endpoint).

---

### `bite.encrypt_transaction(tx: dict) -> dict`

Encrypts a transaction object using the BLS threshold encryption public key(s) from the configured BITE provider. The encrypted transaction will have its `to` field set to the BITE magic address.

- **Parameters**:
  - `tx`: A dictionary containing `data` and `to` fields as hex strings.
- **Returns**: `dict` – The encrypted transaction with modified `data` and `to` fields.

**Encryption Process**:
1. RLP encodes the original `data` and `to` fields
2. Encrypts the encoded data using AES with a randomly generated key
3. Encrypts the AES key using BLS threshold encryption
4. Creates the final payload in RLP format: `[EPOCH_ID, ENCRYPTED_BITE_DATA]`

**Committee Behavior**:
- **Single Committee**: AES key is encrypted with the current BLS public key
- **Dual Committee** (during rotation): AES key is encrypted twice - first with the current committee's key, then with the next committee's key

---

### `bite.encrypt_message(message: str) -> str`

Encrypts a raw hex-encoded message using the BLS threshold encryption from the configured BITE provider.

- **Parameters**:
  - `message`: `str` – The message to encrypt, as a hex string (with or without 0x prefix).
- **Returns**: `str` – The encrypted message.

---

### `bite.get_committees_info() -> List[dict]`

Fetches information about the current and next (if applicable) committees from the BITE provider.

- **Returns**: `List[dict]` – List of committee information objects containing `common_bls_public_key` and `epoch_id`.

---

### `bite.get_decrypted_transaction_data(transaction_hash: str) -> str`

Retrieves decrypted transaction data for a given transaction hash.

- **Parameters**:
  - `transaction_hash`: `str` – The hash of the transaction.
- **Returns**: `str` – The decrypted transaction data.

---

### `BITEMockup`

A mockup version of BITE for testing purposes that simulates encryption without connecting to a real endpoint.

```python
from bite import BITEMockup

async def test():
    bite_mock = BITEMockup()
    encrypted_tx = await bite_mock.encrypt_transaction({
        'to': '0x1234567890123456789012345678901234567890',
        'data': '0x1234567890abcdef'
    })
    print(encrypted_tx)

asyncio.run(test())
```

## Development

### Setup
```bash
# Clone the repository
git clone https://github.com/skalenetwork/bite.py
cd bite.py

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8 .
```

## License
This project is licensed under the GNU Lesser General Public License v3.0 or later (LGPL-3.0-or-later).

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Support
For support, please contact SKALE Labs at support@skalelabs.com or open an issue on GitHub.
