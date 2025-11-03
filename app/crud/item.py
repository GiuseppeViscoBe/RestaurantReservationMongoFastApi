from app.models.item import ItemCreate, ItemUpdate
from bson import ObjectId
from fastapi import HTTPException

def obj_id(id: str):
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

class ItemCRUD:
    def __init__(self, db):
        self.db = db
        self.collection = db["items"]

    async def create(self, item: ItemCreate):
        result = await self.collection.insert_one(item.model_dump())
        data = item.model_dump()
        data["_id"] = str(result.inserted_id)
        return data

    async def list(self, limit: int = 100):
        items = await self.collection.find().to_list(limit)
        for i in items:
            i["_id"] = str(i["_id"])
        return items

    async def get(self, item_id: str):
        item = await self.collection.find_one({"_id": obj_id(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item["_id"] = str(item["_id"])
        return item

    async def update(self, item_id: str, item: ItemUpdate):
        update_data = {k: v for k, v in item.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No data to update")
        result = await self.collection.update_one({"_id": obj_id(item_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        updated_item = await self.collection.find_one({"_id": obj_id(item_id)})
        updated_item["_id"] = str(updated_item["_id"])
        return updated_item

    async def delete(self, item_id: str):
        result = await self.collection.delete_one({"_id": obj_id(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}
