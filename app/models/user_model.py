from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    name: str
    password : str
    email: EmailStr 

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None
    email: EmailStr | None = None

class UserDB(UserBase):
    id: str = Field(..., alias="_id")
