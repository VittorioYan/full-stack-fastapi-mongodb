from app import crud
from app.models.item import ItemCreate, ItemUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_item() -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = create_random_user()
    item = crud.item.create_with_owner(obj_in=item_in, owner_id=user.email)
    assert item.title == title
    assert item.description == description
    assert item.owner_id == user.email


def test_get_item() -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = create_random_user()
    item = crud.item.create_with_owner( obj_in=item_in, owner_id=user.email)
    stored_item = crud.item.get(id=item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.description == stored_item.description
    assert item.owner_id == stored_item.owner_id


def test_update_item() -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = create_random_user()
    item = crud.item.create_with_owner( obj_in=item_in, owner_id=user.email)
    description2 = random_lower_string()
    item_update = ItemUpdate(description=description2)
    item2 = crud.item.update( db_obj=item, obj_in=item_update)
    assert item.id == item2.id
    assert item.title == item2.title
    assert item2.description == description2
    assert item.owner_id == item2.owner_id


def test_delete_item() -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = create_random_user()
    item = crud.item.create_with_owner(obj_in=item_in, owner_id=user.email)
    item2 = crud.item.remove(id=item.id)
    item3 = crud.item.get( id=item.id)
    assert item3 is None
    assert item2.id == item.id
    assert item2.title == title
    assert item2.description == description
    assert item2.owner_id == user.email
