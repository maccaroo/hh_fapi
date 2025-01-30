from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel


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
    created_by_user_id: int
    data_type: str

    class Config:
        from_attributes = True
