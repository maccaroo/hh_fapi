from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreatedByUser(BaseModel):
    id: int
    username: str
    email: str


class SensorBase(BaseModel):
    name: str
    description: Optional[str] = None

class SensorCreate(SensorBase):
    pass

class SensorUpdate(SensorBase):
    name: Optional[str]
    description: Optional[str] = None

class SensorResponse(SensorBase):
    id: int
    created_at: datetime
    created_by_user: CreatedByUser

    class Config:
        from_attributes = True