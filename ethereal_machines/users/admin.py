from django.contrib import admin
from django.contrib.auth.models import Group  # Removing Groups from Admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Custom Admin for the CustomUser model
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

    # List display fields
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    
    # Fields to filter by in the Admin UI
    list_filter = ['role', 'is_active', 'is_staff']

    # Fields to display when editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    # Fields to search by
    search_fields = ('email', 'first_name', 'last_name')
    
    # Default ordering
    ordering = ('email',)

# Register the custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Remove Group Model from the Admin as we don't need it
admin.site.unregister(Group)
