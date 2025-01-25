from pydantic import BaseModel, ConfigDict


class MetaBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str


class MetaCreate(MetaBase):
    meta_type: str


class MetaUpdate(MetaBase):
    name: str

class MetaResponse(MetaBase):
    id: int
    meta_type: str

    class Config:
        from_attributes = True
