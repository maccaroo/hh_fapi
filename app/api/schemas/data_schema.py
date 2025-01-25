from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreatedByUser(BaseModel):
    id: int
    username: str
    email: str


class MetaValue(BaseModel):
    name: str
    value: str


class DataBase(BaseModel):
    name: str
    description: Optional[str] = None


class DataCreate(DataBase):
    data_type: str


class DataUpdate(DataBase):
    name: Optional[str]
    description: Optional[str] = None


class DataResponse(DataBase):
    id: int
    created_at: datetime
    created_by_user: CreatedByUser
    data_type: str

    class Config:
        from_attributes = True
