from bson.objectid import ObjectId
from typing import Any,Union


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other,ObjectId):
            return self.__id == other.binary
        if isinstance(other,str):
            return str(self) == other
        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        if isinstance(other,ObjectId):
            return self.__id != other.binary
        if isinstance(other,str):
            return str(self) != other
        return NotImplemented

