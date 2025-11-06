from datetime import datetime
from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from app.models.reservation_model import ReservationCreate, ReservationUpdate
from app.crud.reservation_crud import ReservationCRUD
from fastapi import Request

router = APIRouter(prefix="/reservations", tags=["reservations"])

def get_reservation_crud(request: Request):
    return ReservationCRUD(request.app.database, request.app.redis)

@router.get("/", response_model=list[dict])
async def list_reservations(
    crud: ReservationCRUD = Depends(get_reservation_crud)
):
    return await crud.list()

@router.get("/by-date", response_model=list[dict])
async def get_reservations_by_date(
    start_date: datetime = Query(..., description="Start datetime in ISO format"),
    end_date: datetime = Query(..., description="End datetime in ISO format"),
    crud: ReservationCRUD = Depends(get_reservation_crud)
):
    return await crud.list_by_date_range(start_date, end_date)

@router.post("/", response_model=dict)
async def create_reservation(reservation: ReservationCreate, crud: ReservationCRUD = Depends(get_reservation_crud)):
    return await crud.create(reservation)

@router.put("/", response_model=dict)
async def update_reservation(reservation: ReservationUpdate, crud: ReservationCRUD = Depends(get_reservation_crud)):
    return await crud.update(reservation)