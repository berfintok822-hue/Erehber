from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Unregister default User admin
admin.site.unregister(User)

# Register User with full permissions including delete
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    
    def has_delete_permission(self, request, obj=None):
        # Enable delete permission for all staff/admin users
        return True
    
    def get_actions(self, request):
        # Get default actions including delete_selected
        actions = super().get_actions(request)
        # Ensure delete is available
        if 'delete_selected' not in actions:
            from django.contrib.admin.actions import delete_selected
            actions['delete_selected'] = (delete_selected, 'delete_selected', delete_selected.short_description)
        return actions
