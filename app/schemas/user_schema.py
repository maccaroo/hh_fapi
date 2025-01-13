from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True