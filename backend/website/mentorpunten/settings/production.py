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
