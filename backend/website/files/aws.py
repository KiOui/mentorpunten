from functools import lru_cache
from typing import Any, Dict

from django.conf import settings
import boto3
from attrs import define


@define
class S3Credentials:
    access_key_id: str
    secret_access_key: str
    region_name: str
    bucket_name: str
    default_acl: str
    presigned_expiry: int
    max_size: int


@lru_cache
def s3_get_credentials() -> S3Credentials:
    return S3Credentials(
        access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
        default_acl=settings.AWS_DEFAULT_ACL,
        presigned_expiry=settings.AWS_PRESIGNED_EXPIRY,
        max_size=settings.FILE_MAX_SIZE,
    )


def s3_get_client():
    credentials = s3_get_credentials()
    return boto3.client(
        service_name="s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )


def s3_generate_presigned_post(*, file_path: str, file_type: str) -> Dict[str, Any]:
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