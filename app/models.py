# from uuid import UUID, uuid4
# from pydantic import Field
# from schemas import UserCreate
# from beanie import Document, Indexed
# from datetime import date
#
#
# # Beanie Document (ODM) model
# class UserInDB(Document, UserCreate):
#     id: Indexed(UUID) = Field(default_factory=uuid4)
#
#     class Settings:
#         # Set the collection name
#         name = "users5"
#         # Set an encoder for the date
#         bson_encoders = {
#             date: str
#         }
