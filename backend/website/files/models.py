import os
import uuid
from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


User = get_user_model()


def get_random_filename(current_filename):
    """Get a random filename by overwriting the filename with a random string."""
    extension = Path(current_filename).suffix
    unique_id = uuid.uuid4()
    return f"{unique_id}{extension}"


def file_upload_to(instance, filename):
    return os.path.join("files", get_random_filename(filename))


class TemporaryFileUpload(models.Model):
    """Temporary File Upload model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    original_file_name = models.CharField(max_length=300)
    file_name = models.CharField(max_length=300, unique=True)
    file_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    finished_at = models.DateTimeField(null=True, blank=True)
    presigned_data = models.JSONField()

    @property
    def finished(self):
        """Whether a Temporary File Upload is finished."""
        return self.finished_at is not None


class File(models.Model):
    """File model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=file_upload_to)

    original_file_name = models.CharField(max_length=300)

    file_name = models.CharField(max_length=300, unique=True)
    file_type = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    temporary_file_upload = models.ForeignKey(
        TemporaryFileUpload, on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def url(self):
        """Get URL of the File."""
        if settings.FILE_UPLOAD_STORAGE == "s3":
            return self.file.url

        return f"{settings.APP_DOMAIN}{self.file.url}"
    
    @property
    def compressed_url(self):
        if settings.FILE_UPLOAD_STORAGE == "s3":
            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/compressed/{self.file_name}"

        return f"{settings.APP_DOMAIN}{self.file.url}"
    
    def __str__(self):
        """Convert this object to string."""
        return self.original_file_name
