import uuid
from pathlib import Path

from files import models

import files.aws as aws
from users.models import User


def get_random_filename(current_filename):
    """Get a random filename by overwriting the filename with a random string."""
    extension = Path(current_filename).suffix
    unique_id = uuid.uuid4()
    return f"{unique_id}{extension}"


def create_temporary_file_upload_data(user: User, file_name: str, file_type: str):
    """Create Temporary File Upload Data."""
    random_filename = get_random_filename(file_name)
    presigned_data = aws.s3_generate_presigned_post(
        models.get_file_location(random_filename), file_type
    )
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
