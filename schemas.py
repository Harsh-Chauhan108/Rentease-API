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

class PropertySchema(BaseModel):
    title: str
    city: str
    rent: int
    description: str

class BookingSchema(BaseModel):
    property_id: int
class PropertyResponse(BaseModel):
    id: int
    title: str
    city: str
    rent: int
    description: str
    class Config:
        from_attributes = True