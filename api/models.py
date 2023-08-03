from typing import Annotated
from beanie import Document, Indexed
from datetime import date
from pydantic import Field, constr
from api.schemas import UserCreate


# Beanie Document (ODM) model
class UserInDB(Document, UserCreate):
    # id: Indexed(PydanticObjectId)
    email: Indexed(Annotated[
                       constr(regex="^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", strip_whitespace=True), Field(
                           example="email@provider.com", description="The email of the user.")], unique=True) = Field()

    class Settings:
        # Set the collection name
        name = "users12121"
        # Set an encoder for the date
        bson_encoders = {
            date: str
        }
