import uuid
from pydantic import BaseModel, Field, EmailStr


# Модель UserSchema
class UserShema(BaseModel):
    id: str
    email: EmailStr # Используем EmailStr вместо str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


# Модель CreateUserRequestSchema
class CreateUserRequestShema(BaseModel):
    email: EmailStr # Используем EmailStr вместо str
    password: str
    last_name : str = Field(alias="lastName")
    first_name : str = Field(alias="firstName")
    middle_name : str = Field(alias="middleName")

# Модель CreateUserResponseSchema
class CreateUserResponseShema(BaseModel):
    user: UserShema
