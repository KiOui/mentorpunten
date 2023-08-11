from botocore.exceptions import ClientError
from django.conf import settings
from django_cron import Schedule, CronJobBase
from files import models

from files.aws import s3_get_client, mediaconvert_compress_file


class RequestCompressionCronJob(CronJobBase):
    """Request compressed files."""

    RUN_EVERY_MINS = 1
    code = "files.request_compression"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def request_compressed_file(self, file: models.File):
        """Request compression of File."""
        try:
            mediaconvert_compress_file(models.get_file_location(file.file_name))
            return True
        except Exception:
            return False

    def do(self):
        """Check for compressed files in Amazon AWS."""
        files_to_check = models.File.objects.filter(
            compressed_file=None, compression_requested=None
        )
        for file in files_to_check:
            if self.request_compressed_file(file):
                models.CompressionRequested.objects.create(file=file)
            else:
                print("Compression request failed for {}".format(file))


class CompressedFileCronJob(CronJobBase):
    """Check for compressed files."""

    RUN_EVERY_MINS = 1
    code = "files.compressed"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def retrieve_compressed_file(self, file: models.File, aws_client=None):
        """Try to retrieve a compressed file."""
        if aws_client is None:
            aws_client = s3_get_client()

        try:
            aws_client.head_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=models.get_compressed_location(file.file_name),
            )
            return True
        except ClientError:
            return False

    def do(self):
        """Check for compressed files in Amazon AWS."""
        files_to_check = models.File.objects.filter(
            compressed_file=None, compression_requested__isnull=False
        )
        aws_client = s3_get_client()
        for file in files_to_check:
            if self.retrieve_compressed_file(file, aws_client=aws_client):
                file.compressed_file = file.compressed_file.field.attr_class(
                    file.compressed_file,
                    file.compressed_file.field,
                    models.get_compressed_location(file.file_name),
                )
                file.save()
                print("Compressed file saved for {}".format(file))
