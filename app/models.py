from beanie import Document, Indexed
from datetime import date
from pydantic import Field
from uuid import UUID, uuid4

from schemas import UserCreate


# Beanie Document (ODM) model
class UserInDB(Document, UserCreate):
    id: Indexed(UUID) = Field(default_factory=uuid4)

    class Settings:
        # Set the collection name
        name = "users5"
        # Set an encoder for the date
        bson_encoders = {
            date: str
        }
