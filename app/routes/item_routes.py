from fastapi import APIRouter, Depends
from app.models.item_model import ItemCreate, ItemUpdate
from app.crud.item_crud import ItemCRUD
from fastapi import Request

router = APIRouter(prefix="/items", tags=["items"])

def get_item_crud(request: Request):
    return ItemCRUD(request.app.database)

@router.post("/", response_model=dict)
async def create_item(item: ItemCreate, crud: ItemCRUD = Depends(get_item_crud)):
    return await crud.create(item)

@router.get("/", response_model=list[dict])
async def list_items(crud: ItemCRUD = Depends(get_item_crud)):
    return await crud.list()

@router.get("/{item_id}", response_model=dict)
async def get_item(item_id: str, crud: ItemCRUD = Depends(get_item_crud)):
    return await crud.get(item_id)

@router.put("/{item_id}", response_model=dict)
async def update_item(item_id: str, item: ItemUpdate, crud: ItemCRUD = Depends(get_item_crud)):
    return await crud.update(item_id, item)

@router.delete("/{item_id}")
async def delete_item(item_id: str, crud: ItemCRUD = Depends(get_item_crud)):
    return await crud.delete(item_id)
