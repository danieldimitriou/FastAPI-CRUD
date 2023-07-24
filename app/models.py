from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from beanie import Document
from typing import Optional
from datetime import date


# Common Base Model
class UserBase(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool = False
    gender: Optional[str]
    date_of_birth: Optional[date]


# Pydantic model for POST data
class UserCreate(UserBase):
    pass


# Pydantic model for the response
class UserOut(UserBase):
    id: UUID
    pass


# Beanie Document (ODM) model
class UserInDB(Document, UserBase):
    id: UUID = Field(default_factory=uuid4)

    class Settings:
        name = "users1"
        bson_encoders = {
            date: str
        }


