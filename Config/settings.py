"""
Django settings for the PropertyCo backend.

Production-ready for Render (web service) + Neon (Postgres) +
any S3-compatible bucket (Backblaze B2 / Cloudflare R2 / Supabase) + Brevo (email API).
Everything environment-specific is read from environment variables.
"""

from pathlib import Path
from datetime import timedelta
import os

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def env_list(name, default=""):
    """Comma-separated env var -> clean list."""
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
IS_DEVELOPMENT = os.getenv("ENVIRONMENT") == "development" or DEBUG

# Render injects RENDER_EXTERNAL_HOSTNAME (e.g. propertyco-api.onrender.com)
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"] + env_list("ALLOWED_HOSTS")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Public URL of the deployed frontend, no trailing slash
# e.g. https://propertyco.vercel.app  (used in email links)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")
# Kept for the password-reset serializer, which expects a bare host
BASE_URL = FRONTEND_URL.split("://", 1)[-1]

# Where "New Partner" notifications go (was sales@propertyco.ng)
SALES_NOTIFICATION_EMAIL = os.getenv("SALES_NOTIFICATION_EMAIL", "propertycosales@gmail.com")


# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'Account',
    'properties',
    'Favorites',
    'Agents',
    'Users',
    'mess',
    'Catalogue',
    'blog',
    'document',
    'requestprop',
    'booking',
    'notifs',
    'partner',
    'rating_history',
    'storages',
    'anymail',
    'pycountry',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Config', 'templates', 'template'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Config.wsgi.application'


# ---------------------------------------------------------------------------
# Database (Neon Postgres via DATABASE_URL; SQLite fallback for local dev)
# ---------------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=60,
        conn_health_checks=True,
    )
}


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'Account.User'
ACCOUNT_ADAPTER = 'Config.adapters.CustomAccountAdapter'

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_RETURN_EXPIRATION': True,
    'JWT_AUTH_COOKIE': 'my-app-auth',
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token',
    'USER_DETAILS_SERIALIZER': 'Account.serializers.UserDetailsSerializer',
    'PASSWORD_RESET_SERIALIZER': 'resetpassword.serializers.CustomPasswordResetSerializer',
    'REGISTER_SERIALIZER': 'Account.serializers.RegisterSerializer',
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'Account.serializers.RegisterSerializer',
}
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'Account.serializers.UserDetailsSerializer',
}
REST_AUTH_TOKEN_MODEL = None

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=24),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}


# ---------------------------------------------------------------------------
# CORS / CSRF
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8080',
] + env_list("CORS_ALLOWED_ORIGINS")   # e.g. https://propertyco.vercel.app
if FRONTEND_URL not in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_URL)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")


# ---------------------------------------------------------------------------
# Security (Render terminates TLS and sets X-Forwarded-Proto)
# ---------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SSL_SECURE_REDIRECT = not IS_DEVELOPMENT
SESSION_COOKIE_SECURE = not IS_DEVELOPMENT
CSRF_COOKIE_SECURE = not IS_DEVELOPMENT
SECURE_SSL_REDIRECT = not IS_DEVELOPMENT
SECURE_HSTS_SECONDS = 31536000 if not IS_DEVELOPMENT else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not IS_DEVELOPMENT
SECURE_HSTS_PRELOAD = not IS_DEVELOPMENT
SECURE_BROWSER_XSS_FILTER = not IS_DEVELOPMENT
SECURE_CONTENT_TYPE_NOSNIFF = not IS_DEVELOPMENT
X_FRAME_OPTIONS = 'DENY'


# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# Static files: served by WhiteNoise from the web service itself
# (admin + Swagger assets). No bucket needed for these.
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ---------------------------------------------------------------------------
# Media files (property photos, avatars, blog images, agent documents)
# S3-compatible bucket. Works with Backblaze B2, Cloudflare R2, Supabase, AWS.
# ---------------------------------------------------------------------------

# Backblaze B2 workaround: newer boto3 versions send checksum headers that
# B2's S3 API can reject. This restores the old behaviour.
os.environ.setdefault('AWS_REQUEST_CHECKSUM_CALCULATION', 'when_required')
os.environ.setdefault('AWS_RESPONSE_CHECKSUM_VALIDATION', 'when_required')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# e.g. https://s3.us-west-004.backblazeb2.com
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL') or None
# e.g. us-west-004
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME') or None

# Endpoint host without scheme, e.g. s3.us-west-004.backblazeb2.com
_endpoint_host = AWS_S3_ENDPOINT_URL.split('://', 1)[-1] if AWS_S3_ENDPOINT_URL else None

# Public hostname files are served from, no scheme.
# Order of precedence:
#   1. AWS_S3_CUSTOM_DOMAIN env var (e.g. a CDN / Cloudflare domain)
#   2. {bucket}.{endpoint host}  -> my-bucket.s3.us-west-004.backblazeb2.com
#   3. {bucket}.s3.amazonaws.com (plain AWS fallback)
if os.getenv('AWS_S3_CUSTOM_DOMAIN'):
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
elif AWS_STORAGE_BUCKET_NAME and _endpoint_host:
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{_endpoint_host}'
elif AWS_STORAGE_BUCKET_NAME:
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
else:
    AWS_S3_CUSTOM_DOMAIN = None

AWS_DEFAULT_ACL = None            # public access is set on the bucket, not per object
AWS_QUERYSTRING_AUTH = False      # plain public URLs, no signed query strings
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = os.getenv('AWS_S3_ADDRESSING_STYLE', 'virtual')
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_LOCATION = 'media'

if AWS_STORAGE_BUCKET_NAME and AWS_ACCESS_KEY_ID:
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    DEFAULT_MEDIA_STORAGE = {"BACKEND": "storages.backends.s3.S3Storage"}
else:
    # Local development without a bucket: keep uploads on disk
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    DEFAULT_MEDIA_STORAGE = {"BACKEND": "django.core.files.storage.FileSystemStorage"}

STORAGES = {
    "default": DEFAULT_MEDIA_STORAGE,
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}


# ---------------------------------------------------------------------------
# Email
# Render's free tier blocks SMTP ports (25/465/587), so Gmail SMTP cannot be
# used there. Brevo's HTTPS API works: verify propertycosales@gmail.com as a
# sender in Brevo and set BREVO_API_KEY.
# ---------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'propertycosales@gmail.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

BREVO_API_KEY = os.getenv('BREVO_API_KEY')
if BREVO_API_KEY:
    EMAIL_BACKEND = 'anymail.backends.brevo.EmailBackend'
    ANYMAIL = {'BREVO_API_KEY': BREVO_API_KEY}
elif os.getenv('EMAIL_USER') and os.getenv('EMAIL_PASS'):
    # Gmail SMTP: fine locally, blocked on Render's free tier
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = os.getenv('EMAIL_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')
    EMAIL_USE_SSL = True
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ---------------------------------------------------------------------------
# API docs
# ---------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    'PERSIST_AUTH': True,
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter your JWT token with `Bearer ` prefix, e.g. Bearer <token>',
        }
    },
}