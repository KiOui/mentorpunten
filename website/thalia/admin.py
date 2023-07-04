from django.contrib import admin
from django.contrib.auth import get_user_model

from thalia.models import ThaliaUser
from users.admin import UserAdmin


User = get_user_model()


class ThaliaUserInline(admin.StackedInline):
    """Thalia User Inline."""

    model = ThaliaUser
    fields = ("thalia_id",)
    readonly_fields = ("thalia_id",)
    extra = 0

    def has_add_permission(self, request, obj):
        """No add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """No change permission."""
        return False

    def has_delete_permission(self, request, obj=None):
        """No delete permission."""
        return False


class ThaliaUserAdmin(UserAdmin):
    """
    Thalia User Admin.

    Add the Thalia User Admin field.
    """

    inlines = [ThaliaUserInline]


admin.site.unregister(User)
admin.site.register(User, ThaliaUserAdmin)
