from django.contrib import admin
from .models import Cafe, MenuItem


# Register your models here.
class CafeAdmin(admin.ModelAdmin):
    """
    Admin for the Cafe Model
    """
    list_display = ['name', 'location', 'opening_time', 'closing_time', 'is_active', 'created_on', 'updated']
    list_display_links = ['name']
    list_filter = ['is_active', 'created_on', 'updated']
    search_fields = ['name', 'location']
    list_editable = ['is_active']
    list_per_page = 10
    ordering = ('-created_on',)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Cafe, CafeAdmin)


class MenuItemAdmin(admin.ModelAdmin):
    """
    Admin for the MenuItem Model
    """
    list_display = ['name', 'cafe', 'price', 'is_available', 'created_on', 'updated']
    list_display_links = ['name']
    list_filter = ['is_available', 'created_on', 'updated']
    search_fields = ['name', 'description', 'cafe__name']
    list_editable = ['is_available']
    list_per_page = 10
    ordering = ('-created_on',)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(MenuItem, MenuItemAdmin)