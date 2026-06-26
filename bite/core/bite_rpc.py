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
BITE Python Library - RPC Client
"""

import asyncio
import re
from typing import Any, Dict, List

import requests

from ..utils import helper, logger


async def get_decrypted_transaction_data(endpoint: str, transaction_hash: str) -> str:
    """
    Fetch decrypted transaction data via JSON-RPC endpoint.

    Args:
        endpoint: BITE URL provider
        transaction_hash: The hash of the transaction to decrypt

    Returns:
        The decrypted transaction data

    Raises:
        ValueError: If endpoint is invalid
        Exception: If RPC request fails
    """
    try:
        helper.validate_url(endpoint)

        request_body = {
            'jsonrpc': '2.0',
            'method': 'bite_getDecryptedTransactionData',
            'params': [transaction_hash],
            'id': 1
        }

        result = await _send_rpc_request(endpoint, request_body)
        return result
    except Exception as error:
        logger.error('Error fetching decrypted transaction data: %s', error)
        raise


async def get_committees_info(endpoint: str) -> List[helper.CommonPublicKeyResponse]:
    """
    Request the committees info via JSON-RPC.

    Args:
        endpoint: BITE URL provider

    Returns:
        List of objects containing the BLS public key and epoch ID

    Raises:
        ValueError: If response is invalid or key format is incorrect
        Exception: If RPC request fails
    """
    try:
        request_body = {
            'jsonrpc': '2.0',
            'method': 'bite_getCommitteesInfo',
            'params': [],
            'id': 1
        }

        result = await _send_rpc_request(endpoint, request_body)

        if not isinstance(result, list):
            raise ValueError('Result is not an array')

        if len(result) == 0 or len(result) > 2:
            raise ValueError(f'Expected array of size 1 or 2, got {len(result)}')

        # Validate each element in the array
        validated_results = []
        for item in result:
            if not isinstance(item, dict):
                raise ValueError('Array element is not an object')

            if 'commonBLSPublicKey' not in item or not isinstance(item['commonBLSPublicKey'], str):
                raise ValueError('commonBLSPublicKey is not a string')

            if 'epochId' not in item or not isinstance(item['epochId'], int):
                raise ValueError('epochId is not a number')

            if not re.match(r'^[0-9a-fA-F]{256}$', item['commonBLSPublicKey']):
                raise ValueError(
                    'commonBLSPublicKey is not a valid 256-character hexadecimal string'
                )

            validated_results.append(
                helper.CommonPublicKeyResponse(item['commonBLSPublicKey'], item['epochId'])
            )

        return validated_results
    except Exception as error:
        logger.error('Error fetching BITE common public key: %s', error)
        raise


async def _send_rpc_request(endpoint: str, request_body: Dict[str, Any]) -> Any:
    """
    Send JSON-RPC request to endpoint.

    Args:
        endpoint: BITE URL provider
        request_body: JSON-RPC request payload

    Returns:
        Result from RPC response

    Raises:
        ValueError: If endpoint is invalid
        Exception: If request fails
    """
    try:
        helper.validate_url(endpoint)

        response = await asyncio.to_thread(
            requests.post,
            endpoint,
            json=request_body,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(f'Received status code: {response.status_code}')

        data = response.json()

        if 'error' in data:
            raise RuntimeError(f"Error from server: {data['error']['message']}")

        return data.get('result')
    except Exception as error:
        logger.error('Error sending RPC request: %s', error)
        raise
