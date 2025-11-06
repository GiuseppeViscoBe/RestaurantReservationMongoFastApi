from fastapi import APIRouter, Depends
from pydantic import EmailStr
from app.models.user_model import UserCreate, UserUpdate
from app.crud.user_crud import UserCRUD
from fastapi import Request

router = APIRouter(prefix="/users", tags=["users"])

def get_user_crud(request: Request):
    return UserCRUD(request.app.database)

@router.post("/", response_model=dict)
async def create_user(user: UserCreate, crud: UserCRUD = Depends(get_user_crud)):
    return await crud.create(user)


@router.get("/", response_model=list[dict])
async def list_users(crud: UserCRUD = Depends(get_user_crud)):
    return await crud.list()

@router.get("/{user_email}", response_model=dict)
async def get_user_by_email(user_email: EmailStr, crud: UserCRUD = Depends(get_user_crud)):
    return await crud.read(user_email)

@router.put("/{user_email}", response_model=dict)
async def update_user(user_email: str, user: UserUpdate, crud: UserCRUD = Depends(get_user_crud)):
    return await crud.update(user_email, user)

@router.delete("/{user_email}")
async def delete_user(user_email: str, crud: UserCRUD = Depends(get_user_crud)):
    return await crud.delete(user_email)