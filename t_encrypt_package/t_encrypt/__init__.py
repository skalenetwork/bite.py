import os
import ctypes
from ctypes import c_char_p

_lib_path = os.path.dirname(os.path.abspath(__file__))

# Load dependencies
for lib in ["libcrypto.so.1.1", "libssl.so.1.1"]:
    lib_file = os.path.join(_lib_path, lib)
    if os.path.exists(lib_file):
        ctypes.CDLL(lib_file, mode=ctypes.RTLD_GLOBAL)

_lib = ctypes.CDLL(os.path.join(_lib_path, "libencrypt.so"))

# encryptMessage
try:
    _encryptMessage = _lib.encryptMessage
    _encryptMessage.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
    _encryptMessage.restype = c_char_p
except AttributeError:
    _encryptMessage = None

def encrypt_message(msg, key, aad_te=None, aad_aes=None):
    if _encryptMessage is None:
        raise NotImplementedError("encryptMessage function not found in libencrypt.so")
    msg_b = msg.encode('utf-8') if isinstance(msg, str) else msg
    key_b = key.encode('utf-8') if isinstance(key, str) and key else (key if key else b'')
    aad_te_b = aad_te.encode('utf-8') if isinstance(aad_te, str) and aad_te else (aad_te if aad_te else None)
    aad_aes_b = aad_aes.encode('utf-8') if isinstance(aad_aes, str) and aad_aes else (aad_aes if aad_aes else None)

    res = _encryptMessage(msg_b, key_b, aad_te_b, aad_aes_b)
    return res.decode('utf-8') if res else None

# encryptMessageDualKey
try:
    _encryptMessageDualKey = _lib.encryptMessageDualKey
    _encryptMessageDualKey.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
    _encryptMessageDualKey.restype = c_char_p
except AttributeError:
    _encryptMessageDualKey = None

def encrypt_message_dual_key(msg, key1, key2, aad_te=None, aad_aes=None):
    if _encryptMessageDualKey is None:
        raise NotImplementedError("encryptMessageDualKey function not found in libencrypt.so")
    msg_b = msg.encode('utf-8') if isinstance(msg, str) else msg
    key1_b = key1.encode('utf-8') if isinstance(key1, str) and key1 else (key1 if key1 else b'')
    key2_b = key2.encode('utf-8') if isinstance(key2, str) and key2 else (key2 if key2 else b'')
    aad_te_b = aad_te.encode('utf-8') if isinstance(aad_te, str) and aad_te else (aad_te if aad_te else None)
    aad_aes_b = aad_aes.encode('utf-8') if isinstance(aad_aes, str) and aad_aes else (aad_aes if aad_aes else None)

    res = _encryptMessageDualKey(msg_b, key1_b, key2_b, aad_te_b, aad_aes_b)
    return res.decode('utf-8') if res else None

# encryptMessageMockup
try:
    _encryptMessageMockup = _lib.encryptMessageMockup
    _encryptMessageMockup.argtypes = [c_char_p]
    _encryptMessageMockup.restype = c_char_p
except AttributeError:
    _encryptMessageMockup = None

def encrypt_message_mockup(msg):
    if _encryptMessageMockup is None:
        raise NotImplementedError("encryptMessageMockup function not found in libencrypt.so")
    msg_b = msg.encode('utf-8') if isinstance(msg, str) else msg
    res = _encryptMessageMockup(msg_b)
    return res.decode('utf-8') if res else None
