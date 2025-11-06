from pydantic import EmailStr
from app.models.user_model import UserCreate, UserUpdate
from bson import ObjectId
from fastapi import HTTPException

def obj_id(id: str):
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

class UserCRUD:
    def __init__(self, db):
        self.collection = db["users"]

    async def create(self, user: UserCreate):
        if await self.collection.find_one({"email" : user.email}):
            raise HTTPException(status_code=400, detail="User already exists")
        
        result = await self.collection.insert_one(user.model_dump())
        data = user.model_dump()
        data["_id"] = str(result.inserted_id)
        return data

    async def list(self, limit: int = 10, skip: int = 0):
        users_cursor = self.collection.find().skip(skip).limit(limit)
        users = [dict(u, _id=str(u["_id"])) async for u in users_cursor]
        return users


    async def read(self, user_email: EmailStr):
        user = await self.collection.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user["_id"] = str(user["_id"])
        return user

    async def update(self, user_email: EmailStr, user: UserUpdate):
        update_data = {k: v for k, v in user.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No data to update")
        result = await self.collection.update_one({"email": user_email}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        updated_user = await self.collection.find_one({"email": user_email})
        updated_user["_id"] = str(updated_user["_id"])
        return updated_user

    async def delete(self, user_email: str):
        result = await self.collection.delete_one({"email": user_email})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
