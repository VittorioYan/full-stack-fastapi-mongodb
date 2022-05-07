import json
import re
from tkinter import N
from pymongo.database import Database
from typing import List, Optional,Union,Dict,Any,TypeVar,Generic,Type
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId

from app.core.security import get_password_hash,verify_password
from app.db.mongodb_utils import get_default_db
from app.crud.utils import doc_result_to_model,doc_results_to_model

from app.models.item import *

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType,CreateSchemaType,UpdateSchemaType]):
    def __init__(self,*,model_indb:Type[ModelType],db:Database,collection:str) -> None:
        self.db=db
        self.collection = self.db[collection]
        self.model = model_indb

    def get(self,id:str) -> Optional[ModelType]:
        result = self.collection.find_one({"_id":ObjectId(id)})
        if result:
            return self.model(**result)
        return result

    def get_multi(self,skip:int=0,limit:int=100)->Optional[List[ModelType]]:
        results = self.collection.find().skip(skip).limit(limit)
        if results:
            return doc_results_to_model(results,self.model)
        return results

    def create(self,obj_in:Type[CreateSchemaType]):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.collection.insert_one(obj_in_data)
        return self.get(db_obj.inserted_id)

    def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data = dict(filter(lambda x:x[1] is not None,update_data.items()))
        self.collection.update_one({'_id':db_obj.id},{'$set':update_data})
        return self.get(db_obj.id)

    def remove(
        self,
        id:str
    ) -> ModelType:
        db_obj = self.get(id)
        self.collection.delete_one({"_id":db_obj.id})
        return db_obj