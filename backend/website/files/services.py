from django.conf import settings
from django.db import transaction
from django.utils import timezone
from files.utils import get_random_filename
from files.utils import file_generate_upload_path
from files.utils import file_generate_local_upload_url

from files.models import File
import files.aws as aws
from users.models import User


class FileUploadService:
    def __init__(self, user: User):
        self.user = user

    @transaction.atomic
    def start(self, *, file_name: str, file_type: str):
        file = File(
            original_file_name=file_name,
            file_name=get_random_filename(file_name),
            file_type=file_type,
            file=None
        )
        file.full_clean()
        file.save()

        upload_path = file_generate_upload_path(file, file.file_name)

        """
        We are doing this in order to have an associated file for the field.
        """
        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()

        presigned_data = {}

        if settings.FILE_UPLOAD_STORAGE == "s3":
            presigned_data = aws.s3_generate_presigned_post(
                file_path=upload_path, file_type=file.file_type
            )
        else:
            presigned_data = {
                "url": file_generate_local_upload_url(file_id=str(file.id)),
            }

        return {"id": file.id, **presigned_data}

    @transaction.atomic
    def finish(self, *, file: File) -> File:
        file.upload_finished_at = timezone.now()

        # Just a guess for when the compression will finish, there should be an endpoint for this later
        file.compression_finished_at = timezone.now() + timezone.timedelta(minutes=2)
        file.full_clean()
        file.save()

        aws.mediaconvert_compress_file(s3_url=file.url)
        return file

    @transaction.atomic
    def upload_local(self, *, file: File, file_obj) -> File:
        file.file = file_obj
        file.full_clean()
        file.save()

        return file