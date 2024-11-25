from datetime import timezone
from django.db import models


# Custom QuerySet for Cafe
class CafeQuerySet(models.query.QuerySet):
    def active(self, *args, **kwargs):
        """
        Get all cafes that are not marked as 'inactive'.
        """
        return super(CafeQuerySet, self).filter(is_active=True)

    def search(self, query):
        """
        Search cafes by name, description, or address.
        """
        lookups = (
            models.Q(name__icontains=query)
            | models.Q(description__icontains=query)
            | models.Q(address__icontains=query)
        )
        return self.filter(lookups).distinct()


# Manager for CafeCategory
class CafeCategoryManager(models.Manager):
    def all(self):
        """
        Get all cafe categories.
        """
        return self.get_queryset()

    def active(self, *args, **kwargs):
        """
        Get all active cafe categories.
        """
        return super(CafeCategoryManager, self).filter(is_active=True)


# Manager for Cafe
class CafeManager(models.Manager):
    def get_queryset(self):
        """
        Get the custom queryset for cafes.
        """
        return CafeQuerySet(self.model, using=self._db)

    def all(self):
        """
        Get all cafes.
        """
        return self.get_queryset()

    def active(self, *args, **kwargs):
        """
        Get all active cafes.
        """
        return self.get_queryset().active()

    def full_search(self, query):
        """
        Perform a full search for cafes based on name, description, or address.
        """
        return self.get_queryset().search(query)

    def filtered_search(self, query):
        """
        Perform a filtered search for active cafes.
        """
        return self.get_queryset().active().search(query)


# Custom QuerySet for MenuItem
class MenuItemQuerySet(models.query.QuerySet):
    def active(self, *args, **kwargs):
        """
        Get all active menu items.
        """
        return super(MenuItemQuerySet, self).filter(is_active=True)

    def search(self, query):
        """
        Search menu items by name, description, or category.
        """
        lookups = (
            models.Q(name__icontains=query)
            | models.Q(description__icontains=query)
            | models.Q(category__name__icontains=query)
        )
        return self.filter(lookups).distinct()


# Manager for MenuItem
class MenuItemManager(models.Manager):
    def get_queryset(self):
        """
        Get the custom queryset for MenuItems.
        """
        return MenuItemQuerySet(self.model, using=self._db)

    def all(self):
        """
        Get all menu items.
        """
        return self.get_queryset()

    def active(self, *args, **kwargs):
        """
        Get only active menu items.
        """
        return self.get_queryset().active()

    def full_search(self, query):
        """
        Perform a full search for menu items based on name, description, or category.
        """
        return self.get_queryset().search(query)

    def filtered_search(self, query):
        """
        Perform a search for active menu items based on name, description, or category.
        """
        return self.get_queryset().active().search(query)
