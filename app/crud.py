from sqlalchemy.orm import Session
from .models import User
from .security import hash_password
from .schemas import UserCreate

def create_user(db: Session, user: UserCreate) -> User:
    hashed = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
