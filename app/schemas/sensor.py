from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SensorBase(BaseModel):
    name: str
    description: Optional[str] = None

class SensorCreate(SensorBase):
    pass

class SensorUpdate(SensorBase):
    name: Optional[str] = None
    description: Optional[str] = None

class Sensor(SensorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True