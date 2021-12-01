from hashlib import pbkdf2_hmac

from app.configs.security_config import security_config
from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_GCM, block_size
from Crypto.Random import get_random_bytes

ITERATIONS = 1024
KEY_LENGTH = 32

_config = security_config()


def encrypt(plaintext: str):
    nonce = get_random_bytes(block_size)
    cipher = AES.new(secret_key(), MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    encrypted = nonce + ciphertext + tag

    return encrypted.hex()


def decrypt(encrypted: str):
    encrypted = bytes.fromhex(encrypted)
    nonce = encrypted[:block_size]
    cipher = AES.new(secret_key(), MODE_GCM, nonce=nonce)
    encrypted, tag = encrypted[block_size:-block_size], encrypted[-block_size:]
    decrypted = cipher.decrypt_and_verify(encrypted, tag)

    return decrypted.decode('utf-8')


def secret_key():
    password = _config.encryption_password.encode('utf-8')
    salt = bytes.fromhex(_config.encryption_salt)

    return pbkdf2_hmac('sha1', password, salt, ITERATIONS, KEY_LENGTH)