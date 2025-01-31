from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel


class DataPointBase(BaseModel):
    created_at: datetime = datetime.now(timezone.utc)
    value: Any

class DataPointCreate(DataPointBase):
    data_id: int

class DataPointResponse(DataPointBase):
    id: int
    data_id: int

    class Config:
        from_attributes = True