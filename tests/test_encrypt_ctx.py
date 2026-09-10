"""
Tests for encrypt_message_for_ctx functionality.
"""
import pytest

from bite import BITE, BITEMockup
from bite.core import encrypt
from bite.utils import helper


class TestEncryptCTX:
    """Tests for encrypt_message_for_ctx."""

    async def test_encrypt_message_for_ctx_valid(self):
        """Test valid encryption for CTX."""
        bite_mock = BITEMockup()
        message = '0x1234567890abcdef'
        ctx_address = '0x1234567890123456789012345678901234567890'

        encrypted = await bite_mock.encrypt_message_for_ctx(message, ctx_address)

        assert encrypted.startswith('0x')
        assert len(encrypted) > len(message)

    async def test_encrypt_message_for_ctx_invalid_address(self):
        """Test invalid address throws error."""
        bite_mock = BITEMockup()
        message = '0x1234567890abcdef'
        ctx_address = '0x1234'

        with pytest.raises(ValueError, match="must be exactly 20 bytes"):
            await bite_mock.encrypt_message_for_ctx(message, ctx_address)

    async def test_encrypt_message_for_ctx_invalid_address_bite(self):
        """Test invalid address throws error for BITE class as well."""
        bite = BITE('https://example.com')
        message = '0x1234567890abcdef'
        ctx_address = '0x1234'

        with pytest.raises(ValueError, match="must be exactly 20 bytes"):
            await bite.encrypt_message_for_ctx(message, ctx_address)

    async def test_encrypt_message_for_ctx_without_0x(self):
        """Test fields without 0x prefix."""
        bite_mock = BITEMockup()
        message = '1234567890abcdef'
        ctx_address = '1234567890123456789012345678901234567890'

        encrypted = await bite_mock.encrypt_message_for_ctx(message, ctx_address)

        assert encrypted.startswith('0x')

    async def test_encrypt_message_rejects_empty_committees(self):
        """Test empty committees raises clear validation error."""
        with pytest.raises(ValueError, match='committees must contain exactly 1 or 2 items'):
            await encrypt.encrypt_message('0x1234567890abcdef', [])

    async def test_encrypt_message_rejects_too_many_committees(self):
        """Test committees list larger than 2 raises clear validation error."""
        committees = [
            helper.CommonPublicKeyResponse('a' * 256, 1),
            helper.CommonPublicKeyResponse('b' * 256, 2),
            helper.CommonPublicKeyResponse('c' * 256, 3),
        ]

        with pytest.raises(ValueError, match='committees must contain exactly 1 or 2 items'):
            await encrypt.encrypt_message('0x1234567890abcdef', committees)
