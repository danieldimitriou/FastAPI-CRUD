import motor.motor_asyncio
import pytest
from beanie import init_beanie
# from mongomock_motor import AsyncMongoMockClient
from app.models import UserInDB


async def init_db():
    # db_name = "users"
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017/users"
    )
    await init_beanie(database=client["user_db"], document_models=[UserInDB])
