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
BITE Python Library - Tests

Basic test suite for the BITE library.
"""

import pytest

from bite import BITEMockup
from bite.utils import constants, helper


class TestHelper:
    """Tests for helper functions."""

    def test_remove_0x_prefix_with_prefix(self):
        """Test removing 0x prefix when present."""
        result = helper.remove_0x_prefix_if_needed('0x1234')
        assert result == '1234'

    def test_remove_0x_prefix_without_prefix(self):
        """Test handling string without 0x prefix."""
        result = helper.remove_0x_prefix_if_needed('1234')
        assert result == '1234'

    def test_validate_hex_string_valid(self):
        """Test validation of valid hex string."""
        # Should not raise exception
        helper.validate_hex_string('1234abcd')
        helper.validate_hex_string('ABCDEF')

    def test_validate_hex_string_invalid_chars(self):
        """Test validation fails for non-hex characters."""
        with pytest.raises(ValueError, match="hexadecimal characters"):
            helper.validate_hex_string('12xyz')

    def test_validate_hex_string_odd_length(self):
        """Test validation fails for odd length."""
        with pytest.raises(ValueError, match="even length"):
            helper.validate_hex_string('123')

    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        helper.validate_url('https://example.com')
        helper.validate_url('http://localhost:8545')

    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        with pytest.raises(ValueError, match="Invalid provider URL"):
            helper.validate_url('not-a-url')


class TestConstants:
    """Tests for constants."""

    def test_bite_address(self):
        """Test BITE address constant."""
        assert constants.BITE_ADDRESS == '0x42495445204D452049274d20454e435259505444'

    def test_default_gas_limit(self):
        """Test default gas limit constant."""
        assert constants.DEFAULT_GAS_LIMIT == 500000


@pytest.mark.asyncio
class TestBITEMockup:
    """Tests for BITEMockup class."""

    def test_encrypt_message_with_0x(self):
        """Test mock message encryption with 0x prefix."""
        bite_mock = BITEMockup()
        message = '0x1234567890abcdef'

        encrypted = bite_mock.encrypt_message(message)

        assert encrypted.startswith('0x')
        assert len(encrypted) > len(message)

    def test_encrypt_message_without_0x(self):
        """Test mock message encryption without 0x prefix."""
        bite_mock = BITEMockup()
        message = '1234567890abcdef'

        encrypted = bite_mock.encrypt_message(message)

        assert encrypted.startswith('0x')
        assert len(encrypted) > len(message)

    def test_encrypt_transaction(self):
        """Test mock transaction encryption."""
        bite_mock = BITEMockup()
        tx = {
            'to': '0x1234567890123456789012345678901234567890',
            'data': '0x1234567890abcdef'
        }

        encrypted_tx = bite_mock.encrypt_transaction(tx)

        assert encrypted_tx['to'] == constants.BITE_ADDRESS
        assert encrypted_tx['data'].startswith('0x')
        assert encrypted_tx['gas_limit'] == constants.DEFAULT_GAS_LIMIT

    def test_encrypt_transaction_with_gas_limit(self):
        """Test mock transaction encryption with custom gas limit."""
        bite_mock = BITEMockup()
        custom_gas = '0x100000'
        tx = {
            'to': '0x1234567890123456789012345678901234567890',
            'data': '0x1234567890abcdef',
            'gas_limit': custom_gas
        }

        encrypted_tx = bite_mock.encrypt_transaction(tx)

        assert encrypted_tx['gas_limit'] == custom_gas

    async def test_encrypt_transaction_invalid_to(self):
        """Test transaction encryption fails with invalid 'to' address."""
        bite_mock = BITEMockup()
        tx = {
            'to': '0x123',  # Too short
            'data': '0x1234567890abcdef'
        }

        with pytest.raises(ValueError):
            await bite_mock.encrypt_transaction(tx)

    async def test_encrypt_transaction_missing_fields(self):
        """Test transaction encryption fails with missing fields."""
        bite_mock = BITEMockup()
        tx = {'data': '0x1234567890abcdef'}  # Missing 'to'

        with pytest.raises(ValueError):
            await bite_mock.encrypt_transaction(tx)
