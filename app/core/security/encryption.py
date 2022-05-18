from hashlib import pbkdf2_hmac

from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_GCM, block_size
from Crypto.Random import get_random_bytes

from app.core.configs.security_config import security_config
from app.core.constants import UTF_8

_ITERATIONS = 1024
_KEY_LENGTH = 32

_config = security_config()
_password = _config.encryption_password.encode(UTF_8)
_salt = bytes.fromhex(_config.encryption_salt)
_key = pbkdf2_hmac("sha256", _password, _salt, _ITERATIONS, _KEY_LENGTH)


def encrypt(plaintext: str):
    nonce = get_random_bytes(block_size)
    cipher = AES.new(_key, MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode(UTF_8))
    encrypted = nonce + ciphertext + tag
    
    return encrypted.hex()


def decrypt(encrypted: str):
    encrypted = bytes.fromhex(encrypted)
    nonce = encrypted[:block_size]
    cipher = AES.new(_key, MODE_GCM, nonce=nonce)
    encrypted, tag = encrypted[block_size:-block_size], encrypted[-block_size:]
    decrypted = cipher.decrypt_and_verify(encrypted, tag)

    return decrypted.decode(UTF_8)
