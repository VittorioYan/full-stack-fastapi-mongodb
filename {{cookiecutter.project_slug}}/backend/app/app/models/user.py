from typing import List, Optional
from pydantic import BaseModel,EmailStr,Field
from bson.objectid import ObjectId

from .base import PyObjectId

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[PyObjectId]= Field(default_factory=PyObjectId, alias="_id")
    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
