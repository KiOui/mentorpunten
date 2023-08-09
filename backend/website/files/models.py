from django.db import models
from django.conf import settings

from files.utils import file_generate_upload_path

class File(models.Model):
    file = models.FileField(
        upload_to=file_generate_upload_path,
        blank=True,
        null=True
    )

    original_file_name = models.TextField()

    file_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=255)

    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        return bool(self.upload_finished_at)

    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == "s3":
            return self.file.url

        return f"{settings.APP_DOMAIN}{self.file.url}"
    
    def __str__(self):
        return self.original_file_name
