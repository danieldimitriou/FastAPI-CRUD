from typing import Annotated
from beanie import Document, Indexed
from datetime import date
from pydantic import Field, constr
from api.schemas import UserCreate


# Beanie Document (ODM) model
class UserInDB(Document, UserCreate):
    class Settings:
        # Set the collection name
        name = "users"
        # Set an encoder for the date
        bson_encoders = {
            date: str
        }
