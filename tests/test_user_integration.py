from app.db import Base, SessionLocal, engine
from app.crud import create_user
from app.schemas import UserCreate
import pytest

@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

def test_create_user_in_db(db):
    user = UserCreate(username="alice", email="alice@example.com", password="pass123")
    created = create_user(db, user)
    assert created.id == 1
    assert created.username == "alice"
