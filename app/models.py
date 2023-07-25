from uuid import UUID, uuid4
from schemas import UserCreate
from pydantic import Field
from beanie import Document, Indexed
from datetime import date


# Beanie Document (ODM) model
class UserInDB(Document, UserCreate):
    id: Indexed(UUID) = Field(default_factory=uuid4)

    class Settings:
        name = "users4"
        bson_encoders = {
            date: str
        }
