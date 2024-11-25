from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from cafe_arna.base_crud import SLUGTYPE, BaseCRUD
from cafes.models import Cafe, MenuItem
from cafes.schema import (
    CreateCafe,
    UpdateCafe,
    CreateMenuItem,
    UpdateMenuItem,
)
from cafe_arna.utils import unique_slug_generator
from django.core.exceptions import ObjectDoesNotExist


class CafeCRUD(BaseCRUD[Cafe, CreateCafe, UpdateCafe, SLUGTYPE]):
    def get(self, slug: SLUGTYPE) -> Optional[Cafe]:
        try:
            query = Cafe.objects.select_related("created_by", "updated_by").get(
                slug=slug
            )
            return query
        except ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail="This cafe does not exist.")

    def get_multiple(self, limit: int = 100, offset: int = 0) -> List[Cafe]:
        query = Cafe.objects.all()[offset : offset + limit]
        if not query:
            raise HTTPException(status_code=404, detail="No cafes found.")
        return list(query)

    def create(self, obj_in: CreateCafe) -> Cafe:
        slug = unique_slug_generator(obj_in.name)
        obj_in = jsonable_encoder(obj_in)
        obj_in["slug"] = slug
        query = Cafe.objects.create(**obj_in)
        return query

    def update(self, obj_in: UpdateCafe, slug: SLUGTYPE) -> Cafe:
        self.get(slug=slug)
        obj_in = jsonable_encoder(obj_in)
        Cafe.objects.filter(slug=slug).update(**obj_in)
        return self.get(slug=slug)

    def delete(self, slug: SLUGTYPE) -> dict:
        Cafe.objects.filter(slug=slug).delete()
        return {"detail": "Successfully deleted!"}


class MenuItemCRUD(BaseCRUD[MenuItem, CreateMenuItem, UpdateMenuItem, SLUGTYPE]):
    def get(self, slug: SLUGTYPE) -> Optional[MenuItem]:
        try:
            query = MenuItem.objects.select_related(
                "cafe", "created_by", "updated_by"
            ).get(slug=slug)
            return query
        except ObjectDoesNotExist:
            raise HTTPException(
                status_code=404, detail="This menu item does not exist."
            )

    def get_multiple(self, limit: int = 100, offset: int = 0) -> List[MenuItem]:
        query = MenuItem.objects.all()[offset : offset + limit]
        if not query:
            raise HTTPException(status_code=404, detail="No menu items found.")
        return list(query)

    def get_by_cafe(self, cafe_slug: SLUGTYPE) -> List[MenuItem]:
        cafe = Cafe.objects.filter(slug=cafe_slug).first()
        if not cafe:
            raise HTTPException(status_code=404, detail="Cafe not found.")
        query = MenuItem.objects.filter(cafe=cafe)
        return list(query)

    def create(self, obj_in: CreateMenuItem) -> MenuItem:
        obj_in = jsonable_encoder(obj_in)
        query = MenuItem.objects.create(**obj_in)
        return query

    def update(self, obj_in: UpdateMenuItem, slug: SLUGTYPE) -> MenuItem:
        self.get(slug=slug)
        obj_in = jsonable_encoder(obj_in)
        MenuItem.objects.filter(slug=slug).update(**obj_in)
        return self.get(slug=slug)

    def delete(self, slug: SLUGTYPE) -> dict:
        MenuItem.objects.filter(slug=slug).delete()
        return {"detail": "Successfully deleted!"}


# CRUD objects
cafe_crud = CafeCRUD(Cafe)
menu_item_crud = MenuItemCRUD(MenuItem)
