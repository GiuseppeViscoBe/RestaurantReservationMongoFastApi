import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DATABASE_NAME", "mydatabase")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
settings = Settings()
