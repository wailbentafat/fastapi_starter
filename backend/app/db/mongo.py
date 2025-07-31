from pymongo import AsyncMongoClient
from app.core.config import settings
from beanie import init_beanie
from app.models.user import User

mongo_client = AsyncMongoClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB]

async def init_mongo():
    await init_beanie(database=mongo_db, document_models=[User])