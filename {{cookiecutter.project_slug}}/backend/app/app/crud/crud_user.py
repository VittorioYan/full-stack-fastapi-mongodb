from pymongo.database import Database
from typing import List, Optional,Union,Dict,Any

from app.core.security import get_password_hash,verify_password
from app.db.mongodb_utils import get_default_db
from app.crud.utils import doc_result_to_model,doc_results_to_model

from app.models.user import UserBase, UserCreate,UserInDB,User,UserUpdate
from .crud_base import CRUDBase

class CRUDUser(CRUDBase[UserInDB,UserCreate,UserUpdate]):
    def get_by_email(self,*,email:str)->Optional[UserInDB]:
        result = self.collection.find_one({'email':email})
        return doc_result_to_model(result,doc_model=UserInDB)

    def create(self, *, obj_in: UserCreate):
        passwordhash = get_password_hash(obj_in.password)
        user = obj_in.dict()
        user['hashed_password'] = passwordhash
        del user['password']
        created_user = super().create(user)
        return created_user

    def update(self, *, email: str, obj_in: UserUpdate) -> User:
        user_in_db = self.get_by_email(email=email)
        user = obj_in.dict()
        if obj_in.password:
            passwordhash = get_password_hash(obj_in.password)
            user['hashed_password'] = passwordhash
            del user['password']
        user_in_db = super().update(user_in_db,user)
        return user_in_db


    def authenticate(self,*, email: str, password: str) -> Optional[UserInDB]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

user = CRUDUser(model_indb=UserInDB,db=get_default_db(),collection='user')