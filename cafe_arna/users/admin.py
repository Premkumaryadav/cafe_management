from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserAdminChangeForm, UserAdminCreationForm

# Unregister the default user admin
admin.site.unregister(get_user_model())

# Register your models here.
User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm

    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}
        ),
    )

    list_display = ('id', 'email', 'get_full_name', 'is_active', 'is_staff')
    list_display_links = ['email']
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')  # search by first and last name
    ordering = ('email',)
    list_per_page = 10
    filter_horizontal = ('groups', 'user_permissions',)

# Customize the admin site
admin.site.site_header = "Arna Cafes Administration"  # The text displayed at the top of each page in the admin
admin.site.site_title = "Arna Cafes Admin"  # The title of the browser tab
admin.site.index_title = "Arna Cafe!"  # The title on the admin index page

admin.site.register(User, UserAdmin)
