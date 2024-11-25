from typing import Any, List
from fastapi import APIRouter
from cafes.cafe_api import cafe_crud, menu_item_crud
from cafes.schema import (
    CafeListOut,
    CafeOut,
    CreateCafe,
    CreateMenuItem,
    MenuItemListOut,
    MenuItemOut,
    UpdateCafe,
    UpdateMenuItem,
)

router = APIRouter()


# Cafes Endpoints
@router.get("/cafes/", response_model=List[CafeListOut])
def get_multiple_cafes(offset: int = 0, limit: int = 10) -> Any:
    """
    Endpoint to get multiple cafes based on offset and limit values.
    """
    return cafe_crud.get_multiple(offset=offset, limit=limit)


@router.post("/cafes/", status_code=201, response_model=CafeOut)
def create_cafe(request: CreateCafe) -> Any:
    """
    Endpoint to create a single cafe.
    """
    return cafe_crud.create(obj_in=request)


@router.get("/cafes/{slug}/", response_model=CafeOut)
def get_cafe(slug: str) -> Any:
    """
    Get a single cafe by slug.
    """
    return cafe_crud.get(slug=slug)


@router.put("/cafes/{slug}/", response_model=CafeOut)
def update_cafe(slug: str, request: UpdateCafe) -> Any:
    """
    Update a single cafe by slug.
    """
    return cafe_crud.update(slug=slug, obj_in=request)


@router.delete("/cafes/{slug}/")
def delete_cafe(slug: str) -> Any:
    """
    Delete a single cafe by slug.
    """
    return cafe_crud.delete(slug=slug)


# Menu Items Endpoints
@router.get("/menu-items/", response_model=List[MenuItemListOut])
def get_multiple_menu_items(offset: int = 0, limit: int = 10) -> Any:
    """
    Endpoint to get multiple menu items based on offset and limit values.
    """
    return menu_item_crud.get_multiple(offset=offset, limit=limit)


@router.post("/menu-items/", status_code=201, response_model=MenuItemOut)
def create_menu_item(request: CreateMenuItem) -> Any:
    """
    Endpoint to create a single menu item.
    """
    return menu_item_crud.create(obj_in=request)


@router.get("/menu-items/{slug}/", response_model=MenuItemOut)
def get_menu_item(slug: str) -> Any:
    """
    Get a single menu item by slug.
    """
    return menu_item_crud.get(slug=slug)


@router.put("/menu-items/{slug}/", response_model=MenuItemOut)
def update_menu_item(slug: str, request: UpdateMenuItem) -> Any:
    """
    Update a single menu item by slug.
    """
    return menu_item_crud.update(slug=slug, obj_in=request)


@router.delete("/menu-items/{slug}/")
def delete_menu_item(slug: str) -> Any:
    """
    Delete a single menu item by slug.
    """
    return menu_item_crud.delete(slug=slug)


@router.get("/cafes/{slug}/menu-items/", response_model=List[MenuItemListOut])
def get_menu_items_by_cafe(slug: str) -> Any:
    """
    Get all menu items for a specific cafe by its slug.
    """
    return menu_item_crud.get_by_cafe(cafe_slug=slug)
