from app.db import Base, SessionLocal, engine
from app.models import Calculation
import pytest

@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

def test_create_calculation(db):
    calc = Calculation(a=10, b=5, type="Add", result=15)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    assert calc.result == 15
