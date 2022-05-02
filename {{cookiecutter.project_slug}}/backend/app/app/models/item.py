from pydantic import BaseModel,Field
from typing import Optional
from bson.objectid import ObjectId

from .base import PyObjectId

# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass

# Properties to return to client
class Item(ItemBase):
    id: Optional[PyObjectId]= Field(default_factory=PyObjectId, alias="_id")
    title: str
    owner_email: str
    
    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# Properties properties stored in DB
class ItemInDB(Item):
    pass
