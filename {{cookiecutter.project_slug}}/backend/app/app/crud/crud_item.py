import json
from pymongo.database import Database
from typing import List, Optional,Union,Dict,Any
from fastapi.encoders import jsonable_encoder

from app.core.security import get_password_hash,verify_password
from app.db.mongodb_utils import get_default_db
from app.crud.utils import doc_result_to_model,doc_results_to_model
from app.crud.crud_base import CRUDBase

from app.models.item import *


class CRUDItem(CRUDBase[ItemInDB,ItemCreate,ItemUpdate]):
    def create_with_owner(
        self, *, obj_in: ItemCreate, owner_id: str
    ) -> Item:
        item_in_data = jsonable_encoder(obj_in)
        item_in_data['owner_id'] = owner_id
        new_item = self.collection.insert_one(item_in_data)
        return self.get(new_item.inserted_id)

    def get_multi_by_owner(
        self, *, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        results = self.collection.find({"owner_id":owner_id}).skip(skip).limit(limit)
        return doc_results_to_model(results,Item)

    

item = CRUDItem(model_indb=ItemInDB,db=get_default_db(),collection='item',)
