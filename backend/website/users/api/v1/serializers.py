from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializers for Users."""

    display_name = serializers.CharField(source="__str__")
    user_permissions = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField)
    def get_user_permissions(self, instance: User):
        """Get user permissions."""
        return [x for x in instance.get_all_permissions()]

    class Meta:
        """Meta class."""

        model = User
        fields = [
            "id",
            "full_name",
            "display_name",
            "profile_image",
            "user_permissions",
        ]
        read_only_fields = [
            "id",
            "full_name",
            "display_name",
            "profile_image",
            "user_permissions",
        ]
