import email
from typing import Optional


from app import crud
from app.models.item import ItemCreate,Item
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_item(owner_id: Optional[int] = None) -> Item:
    if owner_id is None:
        user = create_random_user()
        owner_id = user.email
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    return crud.item.create_with_owner(obj_in=item_in, owner_id=owner_id)
