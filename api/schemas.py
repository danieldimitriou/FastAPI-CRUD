from enum import Enum
from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional, Annotated
from datetime import date


class Role(str, Enum):
    admin = "admin"
    user = "user"


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


# Common Base Model
class UserBase(BaseModel):
    email: Annotated[
        constr(regex="^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", strip_whitespace=True), Field(
            example="email@provider.com", description="The email of the user.")]
    first_name: Annotated[str, Field(min_length=2, max_length=256, example="Daniel")]
    last_name: Annotated[str, Field(min_length=2, max_length=256, example="Dimitriou")]
    # cannot set the default inside the Field() because of a bug that was fixed in pydantic v1.9.1
    role: Annotated[
        Role, Field(description="The role of the user(can be either admin or user).", example="user")] = Role.user
    gender: Annotated[Optional[Gender], Field(description="The users gender", example="male")]
    date_of_birth: Annotated[Optional[date], Field(description="The date of birth of the user.", example="1997-11-19")]


# Pydantic model for POST data
class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=6, max_length=32, description="The password of the user.",
                                   example="strong_!#~password1!#~")]


class UserUpdate(BaseModel):
    email: Optional[Annotated[
        constr(regex="^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", strip_whitespace=True), Field(
            example="email@example.com", description="The email of the user.")]]
    first_name: Annotated[str, Field(min_length=2, max_length=256, example="Daniel")]
    last_name: Annotated[str, Field(min_length=2, max_length=256, example="Dimitriou")]
    # cannot set the default inside the Field() because of a bug that was fixed in pydantic v1.9.1
    role: Annotated[
        Role, Field(description="The role of the user(can be either admin or user).", example="user")] = Role.user
    gender: Annotated[Optional[Gender], Field(description="The users gender", example="male")]
    date_of_birth: Annotated[Optional[date], Field(description="The date of birth of the user.", example="1997-11-19")]
    password: Annotated[str, Field(min_length=6, max_length=32, description="The password of the user.",
                                   example="strong_!#~password1!#~")]


# Pydantic model for the response
class UserOut(UserCreate):
    pass
