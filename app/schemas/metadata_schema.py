from pydantic import BaseModel, ConfigDict


class MetadataBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str


class MetadataCreate(MetadataBase):
    data_type: str


class MetadataUpdate(MetadataBase):
    name: str

class MetadataResponse(MetadataBase):
    id: int
    data_type: str

    class Config:
        from_attributes = True
