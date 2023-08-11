from functools import lru_cache
from typing import Any, Dict

from django.conf import settings
import boto3


class AWSCredentials:
    """AWS Credentials."""

    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        region_name: str,
        bucket_name: str,
        default_acl: str,
        presigned_expiry: int,
        max_size: int,
        mediaconvert_endpoint_url: str,
    ):
        """Initialize AWS Credentials."""
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name
        self.bucket_name = bucket_name
        self.default_acl = default_acl
        self.presigned_expiry = presigned_expiry
        self.max_size = max_size
        self.mediaconvert_endpoint_url = mediaconvert_endpoint_url


@lru_cache
def s3_get_credentials() -> AWSCredentials:
    """Get AWS Credentials from settings."""
    return AWSCredentials(
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AWS_S3_REGION_NAME,
        settings.AWS_STORAGE_BUCKET_NAME,
        settings.AWS_DEFAULT_ACL,
        settings.AWS_PRESIGNED_EXPIRY,
        settings.FILE_MAX_SIZE,
        settings.AWS_MEDIACONVERT_ENDPOINT_URL,
    )


def s3_get_client():
    """Get AWS Client."""
    credentials = s3_get_credentials()
    return boto3.client(
        service_name="s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )


def mediaconvert_get_client():
    """Get mediaconvert client."""
    credentials = s3_get_credentials()
    return boto3.client(
        service_name="mediaconvert",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region_name,
        endpoint_url=credentials.mediaconvert_endpoint_url,
    )


def s3_generate_presigned_post(file_path: str, file_type: str) -> Dict[str, Any]:
    """Generate presigned post in AWS."""
    credentials = s3_get_credentials()
    s3_client = s3_get_client()

    acl = credentials.default_acl
    expires_in = credentials.presigned_expiry

    presigned_data = s3_client.generate_presigned_post(
        credentials.bucket_name,
        file_path,
        Fields={"acl": acl, "Content-Type": file_type},
        Conditions=[
            {"acl": acl},
            {"Content-Type": file_type},
            ["content-length-range", 1, credentials.max_size],
        ],
        ExpiresIn=expires_in,
    )

    return presigned_data


def mediaconvert_compress_file(s3_url: str):
    """Compress mediaconvert file."""
    client = mediaconvert_get_client()

    response = client.create_job(
        JobTemplate=settings.AWS_MEDIACONVERT_TEMPLATE_NAME,
        Role=settings.AWS_MEDIACONVERT_ROLE_ARN,
        Settings={
            "Inputs": [
                {"FileInput": s3_url},
            ]
        },
    )
    return response
