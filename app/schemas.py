from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID

from utils import Role


# Common Base Model
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    role: Role = Role.user
    gender: Optional[str]
    date_of_birth: Optional[date]


# Pydantic model for POST data
class UserCreate(UserBase):
    password: str
    pass


class UserUpdate(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[Role]
    gender: Optional[str]
    date_of_birth: Optional[date]
    password: Optional[str]


# Pydantic model for the response
class UserOut(UserCreate):
    id: UUID
    pass
