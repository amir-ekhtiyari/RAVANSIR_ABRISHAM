"""
Settings for the Ravan Seir Abrisham website.

Every secret and server-specific value comes from environment variables (or a `.env` file next to
manage.py – see `.env.example`). With no `.env`, the project runs in local development mode.
"""

import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv(path):
    """Minimal .env reader (KEY=value per line) so no extra package is needed."""
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(BASE_DIR / '.env')


def env(key, default=''):
    return os.environ.get(key, default)


def env_bool(key, default=False):
    return env(key, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(key, default=''):
    return [item.strip() for item in env(key, default).split(',') if item.strip()]


# --- Core -----------------------------------------------------------------------------------------

DEBUG = env_bool('DJANGO_DEBUG', True)
SECRET_KEY = env('DJANGO_SECRET_KEY', 'django-insecure-local-development-only')
if not DEBUG and SECRET_KEY.startswith('django-insecure'):
    raise RuntimeError('Set DJANGO_SECRET_KEY in the environment for production.')

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,[::1]')
CSRF_TRUSTED_ORIGINS = env_list('DJANGO_CSRF_TRUSTED_ORIGINS')
# Absolute site address for canonical URLs, Open Graph and the sitemap (no trailing slash).
SITE_URL = env('SITE_URL', 'http://127.0.0.1:8000').rstrip('/')
# Admin lives at a configurable path; change it in production.
ADMIN_URL = env('DJANGO_ADMIN_URL', 'admin/').strip('/') + '/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'core',
    'pages',
    'services',
    'contact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ravansir_abrisham.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'ravansir_abrisham.wsgi.application'

# --- Database: SQLite locally, PostgreSQL when POSTGRES_DB is set (pip install "psycopg[binary]") ---

if env('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB'),
            'USER': env('POSTGRES_USER', 'postgres'),
            'PASSWORD': env('POSTGRES_PASSWORD'),
            'HOST': env('POSTGRES_HOST', 'localhost'),
            'PORT': env('POSTGRES_PORT', '5432'),
            'CONN_MAX_AGE': 60,
            'CONN_HEALTH_CHECKS': True,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
if env('REDIS_URL'):
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.redis.RedisCache', 'LOCATION': env('REDIS_URL')}}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Languages: Persian (default, no URL prefix) and English (/en/) ---------------------------

LANGUAGE_CODE = 'fa'
LANGUAGES = [('fa', _('Persian')), ('en', _('English')), ('tr', _('Turkish'))]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# --- Static & media ----------------------------------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    # Hashed file names in production so browsers can cache static files for a long time.
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage' if DEBUG
                    else 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'},
}
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# --- Email (contact form notifications) ----------------------------------------------------------

# SMTP when EMAIL_HOST is set; otherwise emails are printed to the console (development).
if env('EMAIL_HOST'):
    MAILERS = {'default': {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': env('EMAIL_HOST'),
            'port': int(env('EMAIL_PORT', '587')),
            'username': env('EMAIL_HOST_USER'),
            'password': env('EMAIL_HOST_PASSWORD'),
            'use_tls': env_bool('EMAIL_USE_TLS', True),
            'timeout': 10,
        },
    }}
else:
    MAILERS = {'default': {'BACKEND': 'django.core.mail.backends.console.EmailBackend'}}
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', 'website@localhost')
# Who receives a copy of every consultation request (comma separated). Empty = admin panel only.
CONTACT_NOTIFY_EMAILS = env_list('CONTACT_NOTIFY_EMAILS')
CONTACT_RATE_LIMIT = int(env('CONTACT_RATE_LIMIT', '5'))   # requests per IP per hour

# --- Security ------------------------------------------------------------------------------------

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    LANGUAGE_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(env('DJANGO_HSTS_SECONDS', str(60 * 60 * 24 * 30)))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('DJANGO_HSTS_INCLUDE_SUBDOMAINS', False)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO' if not DEBUG else 'WARNING'},
    'loggers': {'contact': {'handlers': ['console'], 'level': 'INFO', 'propagate': False}},
}
