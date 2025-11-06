from datetime import datetime
import json
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
    def __init__(self, db, redis=None):
        self.collection = db["reservations"]
        self.redis = redis
    
    async def list(self, limit: int = 10, skip: int = 0):
        cache_key = f"reservations:{limit}:{skip}"

        # Try Redis cache first
        if self.redis:
            cached = await self.redis.get(cache_key)
            if cached:
                print("♻️ Cache hit for list()")
                print(cached)
                return json.loads(cached)

        reservations_cursor = self.collection.find().skip(skip).limit(limit)
        reservations = [dict(u, _id=str(u["_id"])) async for u in reservations_cursor]

        # Store in cache
        if self.redis:
            print("Storing in cache")
            await self.redis.setex(cache_key, 60, json.dumps(reservations, default=str))  # cache 1 minute

        return reservations

    async def list_by_date_range(self, start_date: datetime, end_date: datetime):
        users_cursor = self.collection.find({"$and": [
        { "reservation_date_start": { "$gte": start_date }},
        { "reservation_date_end": { "$lte": end_date } }
    ]})
        
        reservations = [dict(u, _id=str(u["_id"])) async for u in users_cursor]
        return reservations
    
    async def create(self, reservation: ReservationCreate):
        reservation_count_by_hour = await self.collection.count_documents({"$and": [
        { "reservation_date_start": { "$gte": reservation.reservation_date_start }},
        { "reservation_date_end": { "$lte": reservation.reservation_date_end } }
    ]})
        if reservation_count_by_hour == 5:
            raise HTTPException(status_code=409, detail="No reservations available for that time")
        
        if await self.existing_reservation(reservation):
                raise HTTPException(status_code=409, detail="You have already an existing reservation for today")
        
        result = await self.collection.insert_one(reservation.model_dump())
        data = reservation.model_dump()
        data["_id"] = str(result.inserted_id)
        return data
    
    async def update(self, reservation: ReservationUpdate):
            update_data = {k: v for k, v in reservation.model_dump().items() if v is not None}
            if not update_data:
                raise HTTPException(status_code=400, detail="No data to update")
    
            #migliorare il filtro dell'update
            result = await self.collection.update_one({"email": reservation.email}, {"$set": update_data})
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Reservation not found")
            
            updated_reservation = await self.collection.find_one({"email": reservation.email})
            updated_reservation["_id"] = str(updated_reservation["_id"])
            return updated_reservation
    
    async def existing_reservation(self, reservation: ReservationUpdate):
        existing_reservation = await self.collection.find_one({"email": reservation.email})
        if not reservation:
            return False

        existing_reservation_day = existing_reservation.reservation_date_start.date()
        
        #Esiste già una prenotazione quel giorno
        if existing_reservation_day == reservation.reservation_date_start.date():
            return True