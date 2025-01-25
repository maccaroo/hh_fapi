from typing import Any
from pydantic import BaseModel


class DataMetaBase(BaseModel):
    data_id: int
    meta_id: int
    value: Any


class DataMetaCreate(DataMetaBase):
    pass


class DataMetaUpdate(DataMetaBase):
    value: Any


class DataMetaResponse(DataMetaBase):
    id: int
    data_id: int
    meta_id: int
    value: Any
    
    class Config:
        from_attributes = True