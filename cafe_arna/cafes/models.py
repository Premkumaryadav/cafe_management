from datetime import date, datetime
from django.conf import settings
from django.db import models
from pathlib import Path
from pydantic import AnyUrl
from typing import Any, Callable, List, Union
from .managers import CafeManager, MenuItemManager


def upload_image_path(instance: Any, file_name:str) -> Union[str, Callable, Path]:
    """
    Set up the default thumbnail upload path.
    """
    try:
        ext = file_name.split('.')[-1]
        filename = "%s.%s" %(instance.slug, ext)
        return "cafes_thumbnails/%s/%s" %(instance.slug, filename)
    except Exception as ex:
        raise f'Something went wrong! Please try again to upload the image'


# Create your models here.
class Cafe(models.Model):
    """
    Model for cafes.
    """
    name: str = models.CharField(max_length=200, unique=True)
    location: str = models.CharField(max_length=255)
    slug: str = models.SlugField(unique=True, blank=True)
    opening_time: datetime = models.TimeField()
    closing_time: datetime = models.TimeField()
    is_active: bool = models.BooleanField(default=True)
    thumbnail: Union[AnyUrl, str] = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    created_on: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)

    # Fields to track the user who created and last updated the record
    created_by: Any = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="cafes_created"
    )
    updated_by: Any = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="cafes_updated"
    )

    objects: CafeManager = CafeManager()

    class Meta:
        constraints: List[Any] = [
            models.UniqueConstraint(fields=['name', 'slug'], name='unique_cafe')
        ]
        verbose_name: str = "cafe"
        verbose_name_plural: str = "cafes"
        ordering: List[str] = ["name"]

    def __repr__(self) -> str:
        return f"<Cafe {self.slug}>"

    def __str__(self) -> str:
        return self.name

    def get_thumbnail_url(self) -> Union[Path, str, AnyUrl]:
        timestamp = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return f"{self.thumbnail.url}?enc={timestamp}"
        
    
class MenuItem(models.Model):
    """
    Model for menu items offered by cafes.
    """
    cafe: Any = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name="menu_items"
    )
    name: str = models.CharField(max_length=200)
    description: str = models.TextField(blank=True, null=True)
    price: float = models.DecimalField(max_digits=10, decimal_places=2)
    is_available: bool = models.BooleanField(default=True)
    created_on: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)

    # Fields to track the user who created and last updated the record
    created_by: Any = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="menu_items_created"
    )
    updated_by: Any = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="menu_items_updated"
    )

    objects: MenuItemManager = MenuItemManager()

    class Meta:
        constraints: List[Any] = [
            models.UniqueConstraint(fields=['name', 'cafe'], name='unique_menu_item')
        ]
        verbose_name: str = "menu item"
        verbose_name_plural: str = "menu items"
        ordering: List[str] = ["name"]

    def __repr__(self) -> str:
        return f"<MenuItem {self.name} at {self.cafe.name}>"

    def __str__(self) -> str:
        return self.name