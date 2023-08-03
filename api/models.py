from beanie import Document, Indexed, PydanticObjectId
from datetime import date

from mongoengine import UUIDField
from pydantic import Field
from uuid import UUID, uuid4

from api.schemas import UserCreate


# from api.schemas import UserCreate


# Beanie Document (ODM) model
class UserInDB(Document, UserCreate):
    # id: Indexed(PydanticObjectId)
    email: Indexed(str, unique=True) = Field()

    class Settings:
        # Set the collection name
        name = "users12121"
        # Set an encoder for the date
        bson_encoders = {
            date: str
        }
