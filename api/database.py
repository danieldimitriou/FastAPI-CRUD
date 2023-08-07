import motor.motor_asyncio
from beanie import init_beanie
from api.models import UserInDB


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://localhost:27017/users"
    )
    await init_beanie(database=client["user_db"], document_models=[UserInDB])
