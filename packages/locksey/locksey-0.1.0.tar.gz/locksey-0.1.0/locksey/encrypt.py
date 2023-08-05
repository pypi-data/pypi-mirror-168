# Stolen from https://stackoverflow.com/a/55147077/5516481

import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
ITERATIONS = 100_000


def _derive_key(password: bytes, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend,
    )
    return b64e(kdf.derive(password))


def encrypt(message: str, password: str, iterations: int = ITERATIONS) -> str:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    encrypted_bytes = b64e(
        b"%b%b%b"
        % (
            salt,
            iterations.to_bytes(4, "big"),
            b64d(Fernet(key).encrypt(message.encode("utf8"))),
        )
    )

    return encrypted_bytes.decode("utf-8")


def decrypt(encrypted: str, password: str) -> str:
    token = encrypted.encode("utf-8")
    decoded = b64d(token)
    salt, iteration_bytes, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iteration_bytes, "big")
    key = _derive_key(password.encode("utf-8"), salt, iterations)
    return Fernet(key).decrypt(token).decode("utf-8")
