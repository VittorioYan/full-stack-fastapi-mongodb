from bson.objectid import ObjectId
from typing import Any,Union
from app.models.item import ItemInDB


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


a = ItemInDB(title = '1',description='2',id='6274b6c2b94ec87edf23ca31',owner_id='123@dad.com')
# a = PyObjectId('6274b6c2b94ec87edf23ca31')
print('6274b6c2b94ec87edf23ca31'==a.id)
print(a.id)