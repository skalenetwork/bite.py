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
BITE Python Library - Main BITE Class
"""

from typing import Dict, List

from .core import bite_rpc, encrypt
from .utils import helper


class BITE:
    """
    Main BITE class for interacting with BITE-enabled SKALE chains.

    This class provides methods to encrypt transaction data and messages
    using BLS threshold encryption.
    """

    def __init__(self, provider_url: str):
        """
        Initialize BITE instance.

        Args:
            provider_url: The BITE URL provider (JSON-RPC endpoint)
        """
        self.provider_url = provider_url

    async def encrypt_message(self, message: str) -> str:
        """
        Encrypt a hex-encoded message using BLS public key.

        Args:
            message: Hex string (with or without 0x prefix)

        Returns:
            Encrypted message as hex string

        Raises:
            ValueError: If message is invalid
            Exception: If encryption fails
        """
        return await encrypt.encrypt_message(message, self.provider_url)

    async def encrypt_transaction(self, tx: Dict[str, str]) -> Dict[str, str]:
        """
        Encrypt a transaction object using BLS public key.

        Args:
            tx: The transaction to encrypt (dict with 'to', 'data', optional 'gas_limit')

        Returns:
            The encrypted transaction with modified 'data' and 'to' fields

        Raises:
            ValueError: If transaction is invalid
            Exception: If encryption fails
        """
        return await encrypt.encrypt_transaction(tx, self.provider_url)

    def encrypt_transaction_with_committee_info(
        self,
        tx: Dict[str, str],
        committees: List[helper.CommonPublicKeyResponse]
    ) -> Dict[str, str]:
        """
        Encrypt a transaction object using provided committee info.

        Args:
            tx: The transaction to encrypt (dict with 'to', 'data', optional 'gas_limit')
            committees: List of committee info objects

        Returns:
            The encrypted transaction with modified 'data' and 'to' fields

        Raises:
            ValueError: If transaction or committees are invalid
            Exception: If encryption fails
        """
        return encrypt.encrypt_transaction_with_committee_info(tx, committees)

    async def get_committees_info(self) -> List[helper.CommonPublicKeyResponse]:
        """
        Fetch the committees info from the configured endpoint.

        Returns:
            List of committee information objects

        Raises:
            Exception: If RPC request fails
        """
        return bite_rpc.get_committees_info(self.provider_url)

    async def get_decrypted_transaction_data(self, transaction_hash: str) -> str:
        """
        Get decrypted transaction data using the configured endpoint.

        Args:
            transaction_hash: The hash of the transaction

        Returns:
            The decrypted transaction data

        Raises:
            Exception: If RPC request fails
        """
        return bite_rpc.get_decrypted_transaction_data(
            self.provider_url,
            transaction_hash
        )


class BITEMockup:
    """
    Mockup version of BITE for testing without connecting to a real endpoint.

    This class simulates encryption operations for testing purposes.
    """

    def encrypt_message(self, message: str) -> str:
        """
        Simulate encryption of a hex-encoded message.

        Args:
            message: Hex string (with or without 0x prefix)

        Returns:
            Mock encrypted message as hex string

        Raises:
            ValueError: If message is invalid
        """
        return encrypt.encrypt_message_mockup(message)

    async def encrypt_transaction(self, tx: Dict[str, str]) -> Dict[str, str]:
        """
        Simulate encryption of a transaction object.

        Args:
            tx: The transaction to encrypt (dict with 'to', 'data', optional 'gas_limit')

        Returns:
            The mock encrypted transaction with modified 'data' and 'to' fields

        Raises:
            ValueError: If transaction is invalid
        """
        return await encrypt.encrypt_transaction_mockup(tx)
