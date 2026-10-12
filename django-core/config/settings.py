import base64
from datetime import timedelta
from pathlib import Path
from decouple import config, Csv
from config.logging_config import LOGGING as _LOGGING_BASE

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "django_filters",
    "allauth",
    "allauth.account",
    # local
    "apps.shared",
    "apps.listings",
    "apps.agencies",
    "apps.leads",
    "apps.valuations",
    "apps.billing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config("DB_NAME", default="realestate"),
        "USER": config("DB_USER", default="realestate"),
        "PASSWORD": config("DB_PASSWORD", default="realestate"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default=config("REDIS_URL", default="redis://localhost:6379/0"))
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://localhost:6379/0"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

AUTH_USER_MODEL = "shared.User"

# Argon2 first; PBKDF2 fallback for existing hashes during migration window
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=not DEBUG, cast=bool)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=31536000 if not DEBUG else 0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

# JWT — RS256 when both key env vars are set; HS256 fallback for local dev
_JWT_PRIVATE_KEY_B64 = config("JWT_PRIVATE_KEY_B64", default="")
_JWT_PUBLIC_KEY_B64 = config("JWT_PUBLIC_KEY_B64", default="")

if _JWT_PRIVATE_KEY_B64 and _JWT_PUBLIC_KEY_B64:
    _JWT_ALGORITHM = "RS256"
    _JWT_SIGNING_KEY = base64.b64decode(_JWT_PRIVATE_KEY_B64)
    _JWT_VERIFYING_KEY = base64.b64decode(_JWT_PUBLIC_KEY_B64)
else:
    _JWT_ALGORITHM = "HS256"
    _JWT_SIGNING_KEY = SECRET_KEY
    _JWT_VERIFYING_KEY = None

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": _JWT_ALGORITHM,
    "SIGNING_KEY": _JWT_SIGNING_KEY,
    "VERIFYING_KEY": _JWT_VERIFYING_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "JTI_CLAIM": "jti",
    "TOKEN_OBTAIN_SERIALIZER": "apps.shared.jwt_backend.ImmoviewTokenObtainPairSerializer",
}

# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.shared.authentication.JWTWithMembershipAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.shared.exception_handler.sentry_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "apps.shared.throttling.PublicRateThrottle",
        "apps.shared.throttling.AuthenticatedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"public": "60/min", "authenticated": "300/min"},
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Real Estate MIS API",
    "DESCRIPTION": "Swiss real estate management information system",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = "/mis/"

# Logging — JSON to stdout in production, simple in DEBUG
LOGGING = _LOGGING_BASE
_log_handler = "stdout_simple" if DEBUG else "stdout_json"
LOGGING["root"]["handlers"] = [_log_handler]
for _logger in LOGGING["loggers"].values():
    _logger.setdefault("handlers", [_log_handler])

# Datadog APM — ddtrace patches third-party libs before import when ddtrace-run is used
# When DD_TRACE_ENABLED=false (default in docker-compose), this is a no-op
DD_TRACE_ENABLED = config("DD_TRACE_ENABLED", default="false").lower() == "true"
if DD_TRACE_ENABLED:
    try:
        import ddtrace
        ddtrace.patch_all()
    except ImportError:
        pass

# Sentry
_SENTRY_DSN = config("SENTRY_DSN", default="")
if _SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=_SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=False,
        before_send=lambda event, hint: _strip_pii(event),
    )


def _strip_pii(event: dict) -> dict:
    if "request" in event and "headers" in event["request"]:
        event["request"]["headers"].pop("Authorization", None)
        event["request"]["headers"].pop("Cookie", None)
    return event
