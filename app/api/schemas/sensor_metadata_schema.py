from typing import Any
from pydantic import BaseModel


class SensorMetadataBase(BaseModel):
    sensor_id: int
    metadata_id: int
    value: Any


class SensorMetadataCreate(SensorMetadataBase):
    pass


class SensorMetadataUpdate(SensorMetadataBase):
    value: Any


class SensorMetadataResponse(SensorMetadataBase):
    id: int
    sensor_id: int
    metadata_id: int
    value: Any
    
    class Config:
        from_attributes = True