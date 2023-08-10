import os

from .base import *
from corsheaders.defaults import default_headers


SECRET_KEY = "django-insecure-)75&$s)bp14c@(z5r!-@qw&yjbk=tb7g#ps6=*6kp^4i=#pl=%"

DEBUG = True

ALLOWED_HOSTS = []


# Databases
# https://docs.djangoproject.com/en/3.2/ref/databases/

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Cors configuration
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/(?:api|user/oauth)/.*"
CORS_ALLOW_HEADERS = (
    *default_headers,
    "my-custom-header",
)

# OAuth configuration
OAUTH2_PROVIDER["ALLOWED_REDIRECT_URI_SCHEMES"] = ["http", "https"]

# Email
# https://docs.djangoproject.com/en/3.2/topics/email/

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_DEFAULT_SENDER = "development@example.com"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

THALIA_API_BASE_URI = "http://localhost:8001"
THALIA_API_AUTHORIZATION_ENDPOINT = "/user/oauth/authorize/"
THALIA_API_ACCESS_TOKEN_ENDPOINT = "/user/oauth/token/"
THALIA_API_OAUTH_CLIENT_ID = os.environ.get("THALIA_API_OAUTH_CLIENT_ID")
THALIA_API_OAUTH_CLIENT_SECRET = os.environ.get("THALIA_API_OAUTH_CLIENT_SECRET")
THALIA_API_OAUTH_REDIRECT_URI = "http://localhost:8000/thalia/callback"
THALIA_API_MEMBERS_URL = "/api/v2/members/me"

# S3 storage
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


# AWS Settings
AWS_ACCESS_KEY_ID = "AKIA2Q6WXDVUT544BOO2"
AWS_SECRET_ACCESS_KEY = "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"

# S3 Settings
AWS_S3_REGION_NAME = "eu-west-1"
AWS_STORAGE_BUCKET_NAME = "mentorpunten"
AWS_DEFAULT_ACL = "private"
AWS_PRESIGNED_EXPIRY = 3600
FILE_MAX_SIZE = 536870912  # 512 MB

# MediaConvert Settings
AWS_MEDIACONVERT_TEMPLATE_NAME = "Compress video file"
AWS_MEDIACONVERT_ROLE_ARN = (
    "arn:aws:iam::723615423849:role/service-role/MediaConvert_Default_Role"
)

# Set to "s3" to upload files to s3
FILE_UPLOAD_STORAGE = "s3"
APP_DOMAIN = "http://localhost:8000"
