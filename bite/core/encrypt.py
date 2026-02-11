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
BITE Python Library - Encryption Module
"""

from typing import Any, Dict, List, Optional

import rlp
from skale_te import encrypt_message as lib_encrypt_message
from skale_te import encrypt_message_dual_key as lib_encrypt_message_dual_key
from skale_te import encrypt_message_mockup as lib_encrypt_message_mockup

from ..utils import constants, helper, logger
from . import bite_rpc


class Transaction:
    """Transaction object for encryption."""
    # pylint: disable=too-few-public-methods

    def __init__(self, to: str, data: str, gas_limit: Optional[str] = None):
        self.to = to
        self.data = data
        self.gas_limit = gas_limit

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary representation."""
        result = {
            'to': self.to,
            'data': self.data
        }
        if self.gas_limit is not None:
            result['gas_limit'] = self.gas_limit
        return result


async def encrypt_transaction(tx: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
    """
    Encrypt a transaction using the real BLS key.

    Args:
        tx: The transaction object with 'to' and 'data' fields
        endpoint: BITE URL provider

    Returns:
        Encrypted transaction with modified 'data' and 'to' fields

    Raises:
        ValueError: If transaction validation fails
        Exception: If encryption fails
    """
    try:
        validated_tx = _validate_and_extract_transaction_fields(tx)
        tx_to = validated_tx['to']
        tx_data = validated_tx['data']

        # RLP encode data and to fields
        rlp_encoded_data = _rlp_encode_transaction_data(tx_to, tx_data)

        encrypted_data = await encrypt_message(rlp_encoded_data, endpoint)

        # Set default gas_limit if not set
        bite_gas_limit = tx.get('gas_limit', constants.DEFAULT_GAS_LIMIT)

        return {
            **tx,
            'data': encrypted_data,
            'to': constants.BITE_ADDRESS,
            'gas_limit': bite_gas_limit
        }
    except Exception as error:
        logger.error('Error encrypting transaction: %s', error)
        raise



def encrypt_transaction_with_committee_info(
    tx: Dict[str, Any],
    committees: List[helper.CommonPublicKeyResponse],
    aad_te: Optional[str] = None,
    aad_aes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Encrypt a transaction using provided committee info.

    Args:
        tx: The transaction object with 'to' and 'data' fields
        committees: List of committee info objects
        aad_te: Optional TE Additional Authenticated Data
        aad_aes: Optional AES Additional Authenticated Data

    Returns:
        Encrypted transaction with modified 'data' and 'to' fields

    Raises:
        ValueError: If transaction validation fails or invalid committees
        Exception: If encryption fails
    """
    try:
        validated_tx = _validate_and_extract_transaction_fields(tx)
        tx_to = validated_tx['to']
        tx_data = validated_tx['data']

        rlp_encoded_data = _rlp_encode_transaction_data(tx_to, tx_data)

        sanitized_aad_aes = helper.remove_0x_prefix_if_needed(aad_aes) if aad_aes else None
        sanitized_aad_te = helper.remove_0x_prefix_if_needed(aad_te) if aad_te else None

        if sanitized_aad_aes:
            helper.validate_hex_string(sanitized_aad_aes)
        if sanitized_aad_te:
            helper.validate_hex_string(sanitized_aad_te)

        encrypted_data = encrypt_message_with_committee_info(
            rlp_encoded_data,
            committees,
            sanitized_aad_te,
            sanitized_aad_aes
        )

        bite_gas_limit = tx.get('gas_limit', constants.DEFAULT_GAS_LIMIT)

        return {
            **tx,
            'data': encrypted_data,
            'to': constants.BITE_ADDRESS,
            'gas_limit': bite_gas_limit
        }
    except Exception as error:
        logger.error('Error encrypting transaction with committee info: %s', error)
        raise


def encrypt_message_with_committee_info(
    message: str,
    committees: List[helper.CommonPublicKeyResponse],
    aad_te: Optional[str] = None,
    aad_aes: Optional[str] = None
) -> str:
    """
    Encrypt a message using provided committee info.

    Args:
        message: The message to encrypt as hex string
        committees: List of committee info objects
        aad_te: Optional TE Additional Authenticated Data
        aad_aes: Optional AES Additional Authenticated Data

    Returns:
        The encrypted message as hex string

    Raises:
        ValueError: If validation fails or invalid committees
        Exception: If encryption fails
    """
    try:
        data = helper.remove_0x_prefix_if_needed(message)
        helper.validate_hex_string(data)

        sanitized_aad_aes = helper.remove_0x_prefix_if_needed(aad_aes) if aad_aes else None
        sanitized_aad_te = helper.remove_0x_prefix_if_needed(aad_te) if aad_te else None

        if sanitized_aad_aes:
            helper.validate_hex_string(sanitized_aad_aes)
        if sanitized_aad_te:
            helper.validate_hex_string(sanitized_aad_te)

        if len(committees) == 1:
            encrypted_raw_message = lib_encrypt_message(
                data,
                committees[0].common_bls_public_key,
                sanitized_aad_te,
                sanitized_aad_aes
            )
            rlp_encoded_result = _rlp_encode_message_data([
                committees[0].epoch_id,
                bytes.fromhex(encrypted_raw_message)
            ])
            return f'0x{rlp_encoded_result}'

        if len(committees) == 2:
            encrypted_raw_message = lib_encrypt_message_dual_key(
                data,
                committees[0].common_bls_public_key,
                committees[1].common_bls_public_key,
                sanitized_aad_te,
                sanitized_aad_aes
            )
            rlp_encoded_result = _rlp_encode_message_data([
                committees[0].epoch_id,
                bytes.fromhex(encrypted_raw_message)
            ])
            return f'0x{rlp_encoded_result}'

        raise ValueError(
            'Invalid input: committees array must contain one or two committee info objects'
        )
    except Exception as error:
        logger.error('Error encrypting message with committee info: %s', error)
        raise



def encrypt_transaction_mockup(tx: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypt a transaction using mock encryption.

    Args:
        tx: The transaction object with 'to' and 'data' fields

    Returns:
        Encrypted transaction with modified 'data' and 'to' fields

    Raises:
        ValueError: If transaction validation fails
        Exception: If encryption fails
    """
    try:
        validated_tx = _validate_and_extract_transaction_fields(tx)
        tx_to = validated_tx['to']
        tx_data = validated_tx['data']

        # RLP encode data and to fields
        rlp_encoded_data = _rlp_encode_transaction_data(tx_to, tx_data)

        encrypted_data = encrypt_message_mockup(rlp_encoded_data)

        # Set default gas_limit if not set
        bite_gas_limit = tx.get('gas_limit', constants.DEFAULT_GAS_LIMIT)

        return {
            **tx,
            'data': encrypted_data,
            'to': constants.BITE_ADDRESS,
            'gas_limit': bite_gas_limit
        }
    except Exception as error:
        logger.error('Error encrypting transaction (mockup): %s', error)
        raise


async def encrypt_message(message: str, endpoint: str) -> str:
    """
    Encrypt a raw hex-encoded message using the real BLS key(s).

    Args:
        message: The message to encrypt, as a hex string (with or without 0x prefix)
        endpoint: BITE URL provider

    Returns:
        The encrypted message as hex string

    Raises:
        ValueError: If message validation fails
        Exception: If encryption fails
    """
    try:
        public_key_responses = bite_rpc.get_committees_info(endpoint)
        return encrypt_message_with_committee_info(message, public_key_responses)
    except Exception as error:
        logger.error('Error encrypting message: %s', error)
        raise


async def encrypt_message_for_ctx(
    message: str,
    ctx_submitter_address: str,
    endpoint: str
) -> str:
    """
    Encrypt a message with a submitter address context.

    Args:
        message: The message to encrypt as hex string
        ctx_submitter_address: The submitter address as hex string
        endpoint: BITE URL provider

    Returns:
        Encrypted message as hex string

    Raises:
        ValueError: If input validation fails
        Exception: If encryption fails
    """
    try:
        message = helper.remove_0x_prefix_if_needed(message)
        ctx_submitter_address = helper.remove_0x_prefix_if_needed(
            ctx_submitter_address
        )

        helper.validate_hex_string(message)
        helper.validate_hex_string(ctx_submitter_address)

        if len(ctx_submitter_address) != 40:
            raise ValueError(
                "Invalid input: 'ctx_submitter_address' field must be exactly 20 bytes"
            )

        rlp_encoded_data = _rlp_encode_transaction_data(
            ctx_submitter_address,
            message
        )

        return await encrypt_message(rlp_encoded_data, endpoint)
    except Exception as error:
        logger.error('Error encrypting message for CTX: %s', error)
        raise


def encrypt_message_mockup(message: str) -> str:
    """
    Encrypt a raw hex-encoded message using mock encryption.

    Args:
        message: The message to encrypt, as a hex string (with or without 0x prefix)

    Returns:
        The encrypted message as hex string

    Raises:
        ValueError: If message validation fails
    """
    try:
        data = helper.remove_0x_prefix_if_needed(message)

        if not all(c in '0123456789abcdefABCDEF' for c in data) or len(data) % 2 != 0:
            raise ValueError("Invalid input: message must be valid hex and even length")

        encrypted_raw_message = lib_encrypt_message_mockup(data)
        epoch_id = 0

        # RLP encode epoch_id and encrypted message
        rlp_encoded_result = _rlp_encode_message_data([
            epoch_id,
            bytes.fromhex(encrypted_raw_message)
        ])
        return f'0x{rlp_encoded_result}'
    except Exception as error:
        logger.error('Error encrypting message: %s', error)
        raise


def encrypt_message_for_ctx_mockup(message: str, ctx_submitter_address: str) -> str:
    """
    Encrypt a message with a submitter address context using mock encryption.

    Args:
        message: The message to encrypt as hex string
        ctx_submitter_address: The submitter address as hex string

    Returns:
        Encrypted message as hex string

    Raises:
        ValueError: If input validation fails
        Exception: If encryption fails
    """
    try:
        message = helper.remove_0x_prefix_if_needed(message)
        ctx_submitter_address = helper.remove_0x_prefix_if_needed(
            ctx_submitter_address
        )

        helper.validate_hex_string(message)
        helper.validate_hex_string(ctx_submitter_address)

        if len(ctx_submitter_address) != 40:
            raise ValueError(
                "Invalid input: 'ctx_submitter_address' field must be exactly 20 bytes"
            )

        rlp_encoded_data = _rlp_encode_transaction_data(
            ctx_submitter_address,
            message
        )

        return encrypt_message_mockup(rlp_encoded_data)
    except Exception as error:
        logger.error('Error encrypting message for CTX (mockup): %s', error)
        raise


def _validate_and_extract_transaction_fields(tx: Dict[str, str]) -> Dict[str, str]:
    """
    Validate a transaction object for encryption and extract the fields to be encrypted.

    Args:
        tx: The transaction object containing 'data' and 'to' fields (hex string)

    Returns:
        Dictionary with 'data' and 'to' fields properly validated and formatted
        as hexadecimal strings without the '0x' prefix

    Raises:
        ValueError: If validation fails
    """
    is_valid = (
        tx and isinstance(tx, dict) and
        'data' in tx and 'to' in tx and
        isinstance(tx['data'], str) and
        isinstance(tx['to'], str)
    )

    if not is_valid:
        raise ValueError(
            "Invalid input: Must be an object with 'data' and 'to' fields of type string"
            )

    tx_data = helper.remove_0x_prefix_if_needed(tx['data'])
    tx_to = helper.remove_0x_prefix_if_needed(tx['to'])

    # Validate that the data and to fields contain only hex characters and are of even length
    helper.validate_hex_string(tx_data)
    helper.validate_hex_string(tx_to)

    if len(tx_to) != 40:
        raise ValueError(
            "Invalid input: 'to' field must be exactly 20 bytes (40 hex characters) long"
            )

    return {'data': tx_data, 'to': tx_to}


def _rlp_encode_transaction_data(tx_to: str, tx_data: str) -> str:
    """
    RLP encode transaction data and to address.

    Args:
        tx_to: The transaction to address as hex string (without 0x prefix)
        tx_data: The transaction data as hex string (without 0x prefix)

    Returns:
        RLP encoded data as hex string (without 0x prefix)

    Raises:
        Exception: If RLP encoding fails
    """
    try:
        # Convert hex strings to bytes for RLP encoding
        to_bytes = bytes.fromhex(tx_to)
        data_bytes = bytes.fromhex(tx_data)

        # RLP encode as array [tx_data, tx_to]
        rlp_encoded = rlp.encode([data_bytes, to_bytes])

        # Convert back to hex string without 0x prefix
        return rlp_encoded.hex()
    except Exception as error:
        logger.error('Error RLP encoding transaction data: %s', error)
        raise RuntimeError('Failed to RLP encode transaction data') from error


def _rlp_encode_message_data(data: list) -> str:
    """
    RLP encode array of epoch_id and encrypted message.

    Args:
        data: Array of data to RLP encode (e.g., [epoch_id, encrypted_bytes])

    Returns:
        RLP encoded data as hex string (without 0x prefix)

    Raises:
        Exception: If RLP encoding fails
    """
    try:
        # RLP encode the array
        rlp_encoded = rlp.encode(data)

        # Convert back to hex string without 0x prefix
        return rlp_encoded.hex()
    except Exception as error:
        logger.error('Error RLP encoding message data: %s', error)
        raise RuntimeError('Failed to RLP encode message data') from error
