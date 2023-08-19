import os

from mentorpunten.settings.base import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = False

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
)

ALLOWED_HOSTS = [os.environ.get("DJANGO_ALLOWED_HOST")]

SESSION_COOKIE_SECURE = True


# Databases
# https://docs.djangoproject.com/en/3.2/ref/databases/

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    }
}


# Logging
# https://docs.djangoproject.com/en/3.2/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/mentorpunten/log/django.log",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },  # noqa
    },  # noqa
}

# S3 storage
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"

THALIA_API_BASE_URI = os.environ.get("DJANGO_THALIA_API_BASE_URI")
THALIA_API_AUTHORIZATION_ENDPOINT = os.environ.get(
    "DJANGO_THALIA_API_AUTHORIZATION_ENDPOINT"
)
THALIA_API_ACCESS_TOKEN_ENDPOINT = os.environ.get(
    "DJANGO_THALIA_API_ACCESS_TOKEN_ENDPOINT"
)
THALIA_API_OAUTH_CLIENT_ID = os.environ.get("DJANGO_THALIA_API_OAUTH_CLIENT_ID")
THALIA_API_OAUTH_CLIENT_SECRET = os.environ.get("DJANGO_THALIA_API_OAUTH_CLIENT_SECRET")
THALIA_API_OAUTH_REDIRECT_URI = os.environ.get("DJANGO_THALIA_API_OAUTH_REDIRECT_URI")
THALIA_API_MEMBERS_URL = os.environ.get("DJANGO_THALIA_API_MEMBERS_URL")

AWS_ACCESS_KEY_ID = os.environ.get("DJANGO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("DJANGO_AWS_SECRET_ACCESS_KEY")

# S3 Settings
AWS_S3_REGION_NAME = os.environ.get("DJANGO_AWS_S3_REGION_NAME")
AWS_STORAGE_BUCKET_NAME = os.environ.get("DJANGO_AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = os.environ.get("DJANGO_AWS_DEFAULT_ACL")
AWS_PRESIGNED_EXPIRY = 3600
FILE_MAX_SIZE = 536870912  # 512 MB

# MediaConvert Settings
AWS_MEDIACONVERT_TEMPLATE_NAME = "Compress video file"
AWS_MEDIACONVERT_ROLE_ARN = os.environ.get("DJANGO_AWS_MEDIACONVERT_ROLE_ARN")
AWS_MEDIACONVERT_ENDPOINT_URL = os.environ.get("DJANGO_AWS_MEDIACONVERT_ENDPOINT_URL")

# Photo compression Settings
AWS_PHOTO_COMPRESSION_ROLE_ARN = os.environ.get("DJANGO_AWS_PHOTO_COMPRESSION_ROLE_ARN")

# Set to "s3" to upload files to s3
FILE_UPLOAD_STORAGE = "s3"
APP_DOMAIN = "http://localhost:8000"
