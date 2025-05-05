from pydantic import BaseModel, ConfigDict

class ResourceBase(BaseModel):
    name: str
    description: str | None = None
    capacity: int

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int
    is_available: bool

    model_config = ConfigDict(from_attributes=True)