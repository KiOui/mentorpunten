import os

from .base import *

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
THALIA_API_OAUTH_CLIENT_ID = "3laS0OCOxHp4V8fFwQqFetMv5QRQaVGvrbMVJGjc"
THALIA_API_OAUTH_CLIENT_SECRET = "ExYQ69CMCKxxc0Kr0WUtPfPXBw6m0gXbzqSpNy6wtUEzfTUR6FHtSBAXPttEQVNZxw1ptKwbYcRcHpVX2zthP4obBIWRcRUrAJNlKZGvaa83io1x5XCCfN45IVy0raE5"
THALIA_API_OAUTH_REDIRECT_URI = "http://localhost:8000/thalia/callback"
THALIA_API_MEMBERS_URL = "/api/v2/members/me"
