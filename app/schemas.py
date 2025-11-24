from pydantic import BaseModel, EmailStr , field_validator
from enum import Enum

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class CalculationType(str, Enum):
    Add = "Add"
    Sub = "Sub"
    Multiply = "Multiply"
    Divide = "Divide"

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

    @field_validator("b")
    def no_zero_divide(cls, v, values):
        if "type" in values and values["type"] == "Divide" and v == 0:
            raise ValueError("Division by zero is not allowed")
        return v

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: float | None
    user_id: int | None

    class Config:
        orm_mode = True