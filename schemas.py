from pydantic import BaseModel,EmailStr,field_validator
from typing import Literal

class RegisterSchema(BaseModel):
    name:str
    email:EmailStr
    password:str
    role: Literal['owner', 'tenant']

    @field_validator('role')
    def transform_role(cls, value):
        return value.upper()


class LoginSchema(BaseModel):
    email: EmailStr
    password: str