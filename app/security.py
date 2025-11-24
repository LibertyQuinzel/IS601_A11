# app/security.py
import hashlib
import bcrypt

# bcrypt has a 72-byte limit on the input. To safely support longer
# passwords, we pre-hash the UTF-8 bytes with SHA-256 when the encoded
# password exceeds 72 bytes. This behavior mirrors bcrypt_sha256 but
# keeps explicit control and avoids passlib backend-detection issues.
MAX_BCRYPT_LENGTH = 72  # bcrypt password limit in bytes


def _prepare_password_bytes(password: str) -> bytes:
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    pw_bytes = password.encode("utf-8")
    if len(pw_bytes) > MAX_BCRYPT_LENGTH:
        # replace with raw SHA-256 digest (32 bytes)
        return hashlib.sha256(pw_bytes).digest()
    return pw_bytes


def hash_password(password: str) -> str:
    """Hash a password using bcrypt. Long passwords are pre-hashed with
    SHA-256 to avoid bcrypt's 72-byte limit.

    Returns the bcrypt hash as a UTF-8 string.
    """
    pw = _prepare_password_bytes(password)
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash. Applies the same
    pre-hash rule for long passwords before checking.
    """
    pw = _prepare_password_bytes(password)
    # bcrypt.checkpw expects bytes
    return bcrypt.checkpw(pw, hashed.encode("utf-8"))


# Optional: test helper for long passwords
# (test helper removed; unit tests now cover long-password behavior)
