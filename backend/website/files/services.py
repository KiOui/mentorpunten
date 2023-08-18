import uuid
from pathlib import Path

from django.conf import settings
from django.core.signing import TimestampSigner

from files import models

import files.aws as aws
from users.models import User


def get_random_filename(current_filename):
    """Get a random filename by overwriting the filename with a random string."""
    extension = Path(current_filename).suffix
    unique_id = uuid.uuid4()
    return f"{unique_id}{extension}"


def debug_create_temporary_file_upload_data(user: User, file_name: str, file_type: str):
    """Create Temporary File Upload Data if DEBUG mode is on."""
    if not settings.DEBUG:
        raise Exception("DEBUG mode is not active so this function should not be used.")

    random_filename = get_random_filename(file_name)
    file_location = models.get_file_location(random_filename)
    signer = TimestampSigner()
    signature = signer.sign(file_location)
    presigned_data = {
        "url": file_location,
        "fields": {"debug": True, "signature": signature},
    }
    return models.TemporaryFileUpload.objects.create(
        original_file_name=file_name,
        file_name=random_filename,
        file_type=file_type,
        created_by=user,
        presigned_data=presigned_data,
    )


def create_temporary_file_upload_data(user: User, file_name: str, file_type: str):
    """Create Temporary File Upload Data."""
    random_filename = get_random_filename(file_name)
    file_location = models.get_file_location(random_filename)
    presigned_data = aws.s3_generate_presigned_post(file_location, file_type)
    return models.TemporaryFileUpload.objects.create(
        original_file_name=file_name,
        file_name=random_filename,
        file_type=file_type,
        created_by=user,
        presigned_data=presigned_data,
    )


def create_file_from_temporary_file_upload(
    temporary_file_upload: models.TemporaryFileUpload,
) -> models.File:
    """Create a file from a temporary file upload."""
    file = models.File(
        original_file_name=temporary_file_upload.original_file_name,
        file_name=temporary_file_upload.file_name,
        file_type=temporary_file_upload.file_type,
        created_by=temporary_file_upload.created_by,
        temporary_file_upload=temporary_file_upload,
    )
    file.file = file.file.field.attr_class(
        file, file.file.field, models.get_file_location(temporary_file_upload.file_name)
    )
    file.full_clean()
    file.save()
    return file
