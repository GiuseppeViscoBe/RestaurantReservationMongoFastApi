from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None

class ItemInDB(ItemBase):
    id: str = Field(..., alias="_id")
