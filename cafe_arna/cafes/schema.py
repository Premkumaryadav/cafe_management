from datetime import datetime
from typing import Any, List, Optional, Union
from pydantic import BaseModel, HttpUrl, validator

# Validators for common fields
def confirm_name(value: str) -> str:
    if not value.strip():
        raise ValueError("Name cannot be empty.")
    return value

def confirm_slug(value: str) -> str:
    if not value.strip():
        raise ValueError("Slug cannot be empty.")
    return value

class CafeBase(BaseModel):
    """
    Base fields for cafes.
    """
    name: str
    location: str
    slug: str
    opening_time: datetime
    closing_time: datetime
    is_active: bool
    thumbnail: Optional[Union[HttpUrl, str]] = None

    # Field-level validations
    _confirm_name = validator("name", allow_reuse=True)(confirm_name)
    _confirm_slug = validator("slug", allow_reuse=True)(confirm_slug)

class CreateCafe(CafeBase):
    """
    Fields for creating a cafe.
    """
    ...

class UpdateCafe(CafeBase):
    """
    Fields for updating a cafe.
    """
    updated_by: Optional[Any]

class CafeOut(CafeBase):
    """
    Response schema for a cafe.
    """
    id: int
    created_on: datetime
    updated: datetime
    created_by: Optional[Any]
    updated_by: Optional[Any]

    class Config:
        from_attributes = True

class CafeListOut(BaseModel):
    """
    Response schema for listing cafes with minimal fields.
    """
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True

class MenuItemBase(BaseModel):
    """
    Base fields for menu items.
    """
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool

    # Field-level validations
    _confirm_name = validator("name", allow_reuse=True)(confirm_name)

class CreateMenuItem(MenuItemBase):
    """
    Fields for creating a menu item.
    """
    ...

class UpdateMenuItem(MenuItemBase):
    """
    Fields for updating a menu item.
    """
    updated_by: Optional[Any]

class MenuItemOut(MenuItemBase):
    """
    Response schema for a menu item.
    """
    id: int
    cafe: CafeOut
    created_on: datetime
    updated: datetime
    created_by: Optional[Any]
    updated_by: Optional[Any]

    class Config:
        from_attributes = True

class MenuItemListOut(BaseModel):
    """
    Response schema for listing menu items with minimal fields.
    """
    id: int
    name: str
    price: float
    is_available: bool

    class Config:
        from_attributes = True
