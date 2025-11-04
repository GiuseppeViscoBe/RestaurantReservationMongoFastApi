from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class ReservationBase(BaseModel):
    email: EmailStr 
    reservation_date_start : datetime
    reservation_date_end : datetime


class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    email: EmailStr 
    reservation_date_start : datetime
    reservation_date_end : datetime

class ReservationInDB(ReservationBase):
    id: str = Field(..., alias="_id")
