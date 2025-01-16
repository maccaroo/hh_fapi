from pydantic import BaseModel, ConfigDict


class MetadataBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str


class MetadataCreate(MetadataBase):
    type: str


class MetadataUpdate(MetadataBase):
    name: str

class MetadataResponse(MetadataBase):
    id: int
    type: str

    class Config:
        from_attributes = True
