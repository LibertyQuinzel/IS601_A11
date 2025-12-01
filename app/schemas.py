from pydantic import BaseModel, EmailStr, ConfigDict


# --------------
# USER
# --------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# --------------
# CALCULATIONS
# --------------

class CalculationCreate(BaseModel):
    operation: str
    number1: float
    number2: float
    result: float | None = None


class CalculationRead(BaseModel):
    id: int
    operation: str
    number1: float
    number2: float
    result: float | None

    model_config = ConfigDict(from_attributes=True)


class CalculationUpdate(BaseModel):
    operation: str | None = None
    number1: float | None = None
    number2: float | None = None
    result: float | None = None

