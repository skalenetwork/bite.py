"""
Tests for encrypt_message_for_ctx functionality.
"""
import pytest

from bite import BITEMockup


class TestEncryptCTX:
    """Tests for encrypt_message_for_ctx."""

    def test_encrypt_message_for_ctx_valid(self):
        """Test valid encryption for CTX."""
        bite_mock = BITEMockup()
        message = '0x1234567890abcdef'
        ctx_address = '0x1234567890123456789012345678901234567890'

        encrypted = bite_mock.encrypt_message_for_ctx(message, ctx_address)

        assert encrypted.startswith('0x')
        # It should be longer than message because of encryption and RLP wrapping
        assert len(encrypted) > len(message)

    def test_encrypt_message_for_ctx_invalid_address(self):
        """Test invalid address throws error."""
        bite_mock = BITEMockup()
        message = '0x1234567890abcdef'
        ctx_address = '0x1234' # Too short

        with pytest.raises(ValueError, match="must be exactly 20 bytes"):
            bite_mock.encrypt_message_for_ctx(message, ctx_address)

    def test_encrypt_message_for_ctx_without_0x(self):
        """Test fields without 0x prefix."""
        bite_mock = BITEMockup()
        message = '1234567890abcdef'
        ctx_address = '1234567890123456789012345678901234567890'

        encrypted = bite_mock.encrypt_message_for_ctx(message, ctx_address)

        assert encrypted.startswith('0x')
