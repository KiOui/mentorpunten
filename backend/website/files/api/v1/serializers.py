from rest_framework import serializers

from files import models
from users.api.v1.serializers import UserSerializer


class TemporaryFileUploadSerializer(serializers.ModelSerializer):
    """Temporary File Upload Serializer."""

    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        """Meta class."""

        model = models.TemporaryFileUpload
        fields = (
            "id",
            "original_file_name",
            "file_name",
            "file_type",
            "created_by",
            "created_at",
            "finished_at",
            "presigned_data",
        )
        read_only_fields = (
            "id",
            "file_name",
            "created_at",
            "created_by",
            "presigned_data",
        )


class FileSerializer(serializers.ModelSerializer):
    """File Serializer."""

    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        """Meta class."""

        model = models.File
        fields = (
            "id",
            "file",
            "compressed_file",
            "thumbnail",
            "original_file_name",
            "file_name",
            "file_type",
            "created_by",
            "created_at",
        )
        read_only_fields = (
            "id",
            "file",
            "compressed_file",
            "thumbnail",
            "original_file_name",
            "file_name",
            "file_type",
            "created_at",
            "created_by",
        )
