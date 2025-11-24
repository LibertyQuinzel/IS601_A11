from app.security import hash_password, verify_password
from app.schemas import UserCreate
import pytest

def test_password_hashing_and_verify():
    raw = "mypassword"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed)

def test_user_schema_validation():
    data = {"username": "bob", "email": "wrongemail", "password": "pass123"}
    with pytest.raises(Exception):
        UserCreate(**data)
