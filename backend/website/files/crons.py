from botocore.exceptions import ClientError
from django.conf import settings
from django_cron import Schedule, CronJobBase
from files import models

from files.aws import (
    s3_get_client,
    mediaconvert_compress_file,
    create_compressed_image_job,
)


class RequestCompressionCronJob(CronJobBase):
    """Request compressed files."""

    RUN_EVERY_MINS = 1
    code = "files.request_compression"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def request_compressed_video(self, file: models.File):
        """Request compression of a Video file."""
        try:
            mediaconvert_compress_file(file.url)
            return True
        except Exception as e:
            print("Exception occurred:\n{}".format(e))
            return False

    def request_compressed_photo(self, file: models.File):
        """Request compression of a Photo file."""
        try:
            create_compressed_image_job(file.file_name)
            return True
        except Exception as e:
            print("Exception occurred:\n{}".format(e))
            return False

    def do(self):
        """Check for compressed files in Amazon AWS."""
        files_to_check = models.File.objects.filter(
            compressed_file="", compression_requested__isnull=True
        )
        for file in files_to_check:
            if file.is_video:
                if self.request_compressed_video(file):
                    models.CompressionRequested.objects.create(file=file)
                    models.ThumbnailRequested.objects.create(file=file)
                else:
                    print(
                        "Compression and Thumbnail request failed for {}".format(file)
                    )
            elif file.is_photo:
                if self.request_compressed_photo(file):
                    models.CompressionRequested.objects.create(file=file)
                else:
                    print("Compression request failed for {}".format(file))


class CompressedFileCronJob(CronJobBase):
    """Check for compressed files."""

    RUN_EVERY_MINS = 1
    code = "files.compressed"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def retrieve_compressed_video_file(self, file: models.File, aws_client=None):
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

    def retrieve_compressed_photo_file(self, file: models.File, aws_client=None):
        """Try to retrieve a compressed file."""
        if aws_client is None:
            aws_client = s3_get_client()

        try:
            aws_client.head_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=models.get_compressed_photo_location(file.file_name),
            )
            return True
        except ClientError:
            return False

    def do(self):
        """Check for compressed files in Amazon AWS."""
        files_to_check = models.File.objects.filter(
            compressed_file="", compression_requested__isnull=False
        )
        aws_client = s3_get_client()
        for file in files_to_check:
            if file.is_video:
                if self.retrieve_compressed_video_file(file, aws_client=aws_client):
                    file.compressed_file = file.compressed_file.field.attr_class(
                        file.compressed_file,
                        file.compressed_file.field,
                        models.get_compressed_location(file.file_name),
                    )
                    file.save()
                    print("Compressed file saved for {}".format(file))
            elif file.is_photo:
                if self.retrieve_compressed_photo_file(file, aws_client=aws_client):
                    file.compressed_file = file.compressed_file.field.attr_class(
                        file.compressed_file,
                        file.compressed_file.field,
                        models.get_compressed_photo_location(file.file_name),
                    )
                    file.save()
                    print("Compressed file saved for {}".format(file))


class ThumbnailFileCronJob(CronJobBase):
    """Check for thumbnail files."""

    RUN_EVERY_MINS = 1
    code = "files.thumbnail"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def retrieve_thumbnail_file(self, file: models.File, aws_client=None):
        """Try to retrieve a compressed file."""
        if aws_client is None:
            aws_client = s3_get_client()

        try:
            aws_client.head_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=models.get_thumbnail_location(file.file_name),
            )
            return True
        except ClientError:
            return False

    def do(self):
        """Check for thumbnail files in Amazon AWS."""
        files_to_check = models.File.objects.filter(
            thumbnail="", thumbnail_requested__isnull=False
        )
        aws_client = s3_get_client()
        for file in files_to_check:
            if self.retrieve_thumbnail_file(file, aws_client=aws_client):
                file.thumbnail = file.thumbnail.field.attr_class(
                    file.thumbnail,
                    file.thumbnail.field,
                    models.get_thumbnail_location(file.file_name),
                )
                file.save()
                print("Thumbnail file saved for {}".format(file))
