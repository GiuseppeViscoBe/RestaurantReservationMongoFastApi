from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncMongoClient(settings.MONGO_URL)
    app.database = app.mongodb_client[settings.DB_NAME]
    print("✅ Connected to MongoDB (async)")
    yield
    await app.mongodb_client.close()
    print("🛑 Disconnected from MongoDB")

def get_database(request):
    return request.app.database
