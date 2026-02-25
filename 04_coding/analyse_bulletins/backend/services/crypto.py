import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _get_fernet() -> Fernet:
    secret_key = os.getenv("SECRET_KEY", "change-me-in-production")
    salt = b"bulletins_salt_v1"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
    return Fernet(key)


def encrypt(data: str) -> bytes:
    return _get_fernet().encrypt(data.encode())


def decrypt(data: bytes) -> str:
    return _get_fernet().decrypt(data).decode()
