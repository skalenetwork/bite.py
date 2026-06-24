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
from t_encrypt import encrypt_message as lib_encrypt_message
from t_encrypt import encrypt_message_dual_key as lib_encrypt_message_dual_key
from t_encrypt import encrypt_message_mockup as lib_encrypt_message_mockup

from ..utils import constants, helper, logger


async def encrypt_transaction(
    tx: Dict[str, Any],
    committees: List[helper.CommonPublicKeyResponse],
    aad_te: Optional[str] = None,
    aad_aes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Encrypt a transaction using the real BLS key.

    Args:
        tx: The transaction object with 'to' and 'data' fields
        committees: The committees info object
        aad_te: Optional TE Additional Authenticated Data
        aad_aes: Optional AES Additional Authenticated Data

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

        rlp_encoded_data = _rlp_encode_transaction_data(tx_to, tx_data)

        encrypted_data = await encrypt_message(
            rlp_encoded_data, committees, aad_te, aad_aes
        )

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


async def encrypt_transaction_mockup(tx: Dict[str, Any]) -> Dict[str, Any]:
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

        rlp_encoded_data = _rlp_encode_transaction_data(tx_to, tx_data)

        encrypted_data = await encrypt_message_mockup(rlp_encoded_data)

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


async def encrypt_message(
    message: str,
    committees: List[helper.CommonPublicKeyResponse],
    aad_te: Optional[str] = None,
    aad_aes: Optional[str] = None
) -> str:
    """
    Encrypt a raw hex-encoded message using the real BLS key(s).

    Args:
        message: The message to encrypt, as a hex string (with or without 0x prefix)
        committees: The committees info object
        aad_te: Optional TE Additional Authenticated Data, as a hex string
        aad_aes: Optional AES Additional Authenticated Data, as a hex string

    Returns:
        The encrypted message as hex string

    Raises:
        ValueError: If message validation fails
        Exception: If encryption fails
    """
    try:
        data = helper.remove_0x_prefix_if_needed(message)
        helper.validate_hex_string(data)

        sanitized_aad_te = (
            helper.remove_0x_prefix_if_needed(aad_te) if aad_te else None
        )
        sanitized_aad_aes = (
            helper.remove_0x_prefix_if_needed(aad_aes) if aad_aes else None
        )

        if sanitized_aad_aes:
            helper.validate_hex_string(sanitized_aad_aes)
        if sanitized_aad_te:
            helper.validate_hex_string(sanitized_aad_te)

        if len(committees) not in (1, 2):
            raise ValueError('Invalid input: committees must contain exactly 1 or 2 items')

        if len(committees) == 1:
            public_key_response = committees[0]
            # pylint: disable=E1121
            encrypted_raw_message = lib_encrypt_message(
                data,
                public_key_response.common_bls_public_key,
                sanitized_aad_te,
                sanitized_aad_aes
            )

            rlp_encoded_result = _rlp_encode_message_data([
                public_key_response.epoch_id,
                bytes.fromhex(encrypted_raw_message)
            ])
            return f'0x{rlp_encoded_result}'
        # pylint: disable=E1121
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
    except Exception as error:
        logger.error('Error encrypting message: %s', error)
        raise


async def encrypt_message_mockup(message: str) -> str:
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

        rlp_encoded_result = _rlp_encode_message_data([
            epoch_id,
            bytes.fromhex(encrypted_raw_message)
        ])
        return f'0x{rlp_encoded_result}'
    except Exception as error:
        logger.error('Error encrypting message: %s', error)
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
        to_bytes = bytes.fromhex(tx_to)
        data_bytes = bytes.fromhex(tx_data)

        rlp_encoded = rlp.encode([data_bytes, to_bytes])

        return rlp_encoded.hex()
    except Exception as error:
        logger.error('Error RLP encoding transaction data: %s', error)
        raise RuntimeError('Failed to RLP encode transaction data') from error


def _rlp_encode_message_data(data: List[Any]) -> str:
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
        rlp_encoded = rlp.encode(data)

        return rlp_encoded.hex()
    except Exception as error:
        logger.error('Error RLP encoding message data: %s', error)
        raise RuntimeError('Failed to RLP encode message data') from error
