from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from beanie import Document, Indexed
from typing import Optional
from datetime import date


# Common Base Model
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_admin: bool = False
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
    is_admin: bool = False
    gender: Optional[str]
    date_of_birth: Optional[date]
    password: Optional[str]


# Pydantic model for the response
class UserOut(UserCreate):
    id: UUID
    pass


# Beanie Document (ODM) model
class UserInDB(Document, UserCreate):
    id: Indexed(UUID) = Field(default_factory=uuid4)

    class Settings:
        name = "users2"
        bson_encoders = {
            date: str
        }


