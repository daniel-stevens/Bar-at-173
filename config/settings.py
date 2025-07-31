# bar_at_173/settings.py (excerpt)
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '<<your-dev-secret>>')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',             # our app
    # 'django_htmx',    # optional, to easily detect HTMX requests
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    #  🔽 these two were missing
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # WhiteNoise stays if you’re using it:
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# Silence the AutoField warnings (Django 3.2+ best practice)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


ROOT_URLCONF = 'config.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # we will put templates in app directories
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'


# Database: using PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'barat173'),
        'USER': os.environ.get('POSTGRES_USER', 'baruser'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'         # for collectstatic in production
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'                # for user-uploaded avatars

AUTH_USER_MODEL = 'core.User'  # use our custom User model
