from django.contrib.auth import get_user_model
from import_export import resources


User = get_user_model()


class UserResource(resources.ModelResource):
    """User Resource."""

    class Meta:
        """Meta class."""

        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "first_name",
            "last_name",
            "profile_image",
            "is_staff",
            "is_superuser",
        )
        export_order = (
            "id",
            "username",
            "full_name",
            "first_name",
            "last_name",
            "profile_image",
            "is_staff",
            "is_superuser",
        )
