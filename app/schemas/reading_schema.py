from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel


class ReadingBase(BaseModel):
    created_at: datetime = datetime.now(timezone.utc)
    value: float
    extra_metadata: Optional[Any] = None

class ReadingCreate(ReadingBase):
    sensor_id: int

class ReadingResponse(ReadingBase):
    id: int
    sensor_id: int

    class Config:
        from_attributes = True