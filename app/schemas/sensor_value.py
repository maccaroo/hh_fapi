from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel


class SensorValueBase(BaseModel):
    recorded_at: datetime = datetime.now(timezone.utc)
    value: float
    extra_metadata: Optional[Any] = None

class SensorValueCreate(SensorValueBase):
    sensor_id: int

class SensorValue(SensorValueBase):
    id: int
    sensor_id: int

    class Config:
        from_attributes = True