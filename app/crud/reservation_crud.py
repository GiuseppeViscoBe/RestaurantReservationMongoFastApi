from datetime import datetime
from pydantic import EmailStr
from app.models.reservation_model import ReservationCreate, ReservationUpdate
from bson import ObjectId
from fastapi import HTTPException

def obj_id(id: str):
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    

class ReservationCRUD:
    def __init__(self, db):
        self.collection = db["reservations"]

    
    async def list(self, limit: int = 10, skip: int = 0):
        reservations_cursor = self.collection.find().skip(skip).limit(limit)
        reservations = [dict(u, _id=str(u["_id"])) async for u in reservations_cursor]
        return reservations


    async def create(self, reservation: ReservationCreate):
        reservation_count_by_hour = await self.collection.count_documents({"$and": [
        { "reservation_date_start": { "$gte": reservation.reservation_date_start }},
        { "reservation_date_end": { "$lte": reservation.reservation_date_end } }
    ]})
        if reservation_count_by_hour == 5:
            raise HTTPException(status_code=400, detail="No reservations available for that time")
        
        result = await self.collection.insert_one(reservation.model_dump())
        data = reservation.model_dump()
        data["_id"] = str(result.inserted_id)
        return data

    async def list_by_date_range(self, start_date: datetime, end_date: datetime):
        users_cursor = self.collection.find({"$and": [
        { "reservation_date_start": { "$gte": start_date }},
        { "reservation_date_end": { "$lte": end_date } }
    ]})
        
        reservations = [dict(u, _id=str(u["_id"])) async for u in users_cursor]
        return reservations