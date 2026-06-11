"""
Stub implementation of t_encrypt for Ubuntu 22 builds.
This provides the expected interface but with limited functionality.
"""

def encrypt_message(message: str, public_key: str) -> str:
    """
    Mock implementation of encrypt_message for Ubuntu 22 builds.
    This should be replaced with the actual t_encrypt implementation.
    """
    raise NotImplementedError("t_encrypt encrypt_message not available in Ubuntu 22 build")

def encrypt_message_dual_key(message: str, public_key1: str, public_key2: str) -> str:
    """
    Mock implementation of encrypt_message_dual_key for Ubuntu 22 builds.
    This should be replaced with the actual t_encrypt implementation.
    """
    raise NotImplementedError("t_encrypt encrypt_message_dual_key not available in Ubuntu 22 build")

def encrypt_message_mockup(message: str) -> str:
    """
    Mock implementation for testing purposes.
    Returns a simple encoded version that can be used for testing.
    """
    # Return a simple mock encryption for testing
    import base64
    return base64.b64encode(f"MOCK_ENCRYPTED:{message}".encode()).decode()
