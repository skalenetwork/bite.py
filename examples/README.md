# BITE Python Library - Examples

This directory contains examples demonstrating how to use the bite-py library.

## Examples

### Basic Transaction Encryption
**File:** `basic_transaction_encryption.py`

Demonstrates how to encrypt a transaction using the BITE protocol.

```bash
python basic_transaction_encryption.py
```

### Message Encryption
**File:** `message_encryption.py`

Shows how to encrypt a raw hex-encoded message.

```bash
python message_encryption.py
```

### Mockup Encryption for Testing
**File:** `mockup_encryption.py`

Demonstrates using the BITEMockup class for testing without a real endpoint.

```bash
python mockup_encryption.py
```

## Requirements

Before running the examples, install the bite-py package:

```bash
pip install -e ..
```

Or if you have the package installed from PyPI:

```bash
pip install bite-py
```

## Configuration

Replace the `provider_url` in the examples with your actual BITE JSON-RPC endpoint URL.

For testing without a real endpoint, use the `BITEMockup` class as shown in `mockup_encryption.py`.
