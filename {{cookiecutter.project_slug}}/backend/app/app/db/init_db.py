import logging

from app.core.config import settings
from app.db.mongodb_utils import get_default_db
from app import crud
from app.models.user import UserCreate

def init_db():
    user = crud.user.get_by_email(email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(user_in=user_in)
    
