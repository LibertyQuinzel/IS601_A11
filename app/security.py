from passlib.context import CryptContext
MAX_BCRYPT_LENGTH = 72  # bcrypt limit

def truncate_password(password: str) -> str:
    return password[:MAX_BCRYPT_LENGTH]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    truncated_password = truncate_password(password)
    return pwd_context.hash(truncated_password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)
