from pathlib import Path

from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "mentorpunten",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_bootstrap5",
    "tinymce",
    "fontawesomefree",
    "autocompletefilter",
    "import_export",
    "rest_framework",
    "django_filters",
    "rangefilter",
    "mentorpunten.django_cron_app_config.CustomDjangoCronAppConfig",
    "announcements",
    "users",
    "thalia",
    "transactions",
    "tournaments",
    "challenges",
    "oauth2_provider",
    "corsheaders",
    "files",
]

AUTH_USER_MODEL = "users.User"

ANONYMOUS_USER_NAME = None

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)  # default

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "announcements.middleware.ClosedAnnouncementsMiddleware",
    "announcements.middleware.AppAnnouncementMiddleware",
]

ROOT_URLCONF = "mentorpunten.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mentorpunten.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_SCHEMA_CLASS": "mentorpunten.api.openapi.CustomAutoSchema",
}

# S3 storage
STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/(?:api|user/oauth)/.*"

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000

# OAUTH
OAUTH2_PROVIDER = {
    "ALLOWED_REDIRECT_URI_SCHEMES": ["https"],
    "SCOPES": {
        "read": "Authenticated read access to the backend",
        "write": "Authenticated write access to the backend",
    },
}

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Messages
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info info",
    messages.INFO: "alert-info info",
    messages.SUCCESS: "alert-success success",
    messages.WARNING: "alert-warning warning",
    messages.ERROR: "alert-danger danger",
}

# Sites app
SITE_ID = 1

CRON_CLASSES = [
    "files.crons.CompressedFileCronJob",
]

DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 14
