from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient  # correct async Mongo client
import redis.asyncio as redis
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # MongoDB
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.database = app.mongodb_client[settings.DB_NAME]
    print("✅ Connected to MongoDB")

    # Redis
    app.redis = await redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    print("✅ Connected to Redis")

    yield

    # Shutdown
    await app.mongodb_client.close()
    await app.redis.close()
    print("🛑 Disconnected from MongoDB and Redis")
