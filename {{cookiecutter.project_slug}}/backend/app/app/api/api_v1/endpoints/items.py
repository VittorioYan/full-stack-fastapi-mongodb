from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.models.item import *
from app.models.user import User
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            owner_id=current_user.email, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=Item)
def create_item(
    *,
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.item.create_with_owner(obj_in=item_in, owner_id=current_user.email)
    return item


@router.put("/{id}", response_model=Item)
def update_item(
    *,
    id: str,
    item_in: ItemUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = crud.item.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.email):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.update(db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=Item)
def read_item(
    *,
    id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.email):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.delete("/{id}", response_model=Item)
def delete_item(
    *,
    id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.item.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.email):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.remove(id=id)
    return item
