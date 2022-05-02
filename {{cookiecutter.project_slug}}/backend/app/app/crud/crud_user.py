from pymongo.database import Database
from typing import List, Optional,Union,Dict,Any

from app.core.security import get_password_hash,verify_password
from app.db.mongodb_utils import get_default_db
from app.crud.utils import doc_result_to_model,doc_results_to_model

from app.models.user import UserCreate,UserInDB,User,UserUpdate

class CRUDUser():
    db = get_default_db()
    
    def get_by_email(self,*,email:str)->Optional[UserInDB]:
        result = self.db.user.find_one({'email':email})
        return doc_result_to_model(result,doc_model=UserInDB)

    def get_by_id(self,*,id:str)->Optional[UserInDB]:
        result = self.db.user.find_one({'_id':id})
        return doc_result_to_model(result,doc_model=User)

    def create(self, *, user_in: UserCreate):
        passwordhash = get_password_hash(user_in.password)
        user = UserInDB(**user_in.dict(), hashed_password=passwordhash)
        self.db.user.insert_one(user.dict())
        return user

    def update(self, *, email: str, user_in: UserUpdate) -> User:
        stored_user = self.get_by_email(email=email)
        stored_user = stored_user.copy(update=user_in.dict(skip_defaults=True))
        if user_in.password:
            passwordhash = get_password_hash(user_in.password)
            stored_user.hashed_password = passwordhash
        stored_user = UserInDB(**stored_user.dict())
        self.db.user.update_one({'email':stored_user.email},{'$set':stored_user.dict()})
        return stored_user

    def get_multi(self,*,skip:int,limit:int)->List[UserInDB]:
        results = self.db.user.find().skip(skip).limit(limit)
        return doc_results_to_model(results,UserInDB)

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

user = CRUDUser()