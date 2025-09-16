import os
from pathlib import Path

# -------------------------
# Base Directory
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# Secret Key & Debug
# -------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change_this_in_production")
DEBUG = True
ALLOWED_HOSTS = []

# -------------------------
# Installed Apps
# -------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core",
    "apps.users",
    "apps.billing",
    "apps.api",
    "rest_framework",
]

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------
# URL Configuration
# -------------------------
ROOT_URLCONF = "droom_demo.urls"

# -------------------------
# Templates
# -------------------------
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

# -------------------------
# WSGI & ASGI
# -------------------------
WSGI_APPLICATION = "droom_demo.wsgi.application"
ASGI_APPLICATION = "droom_demo.asgi.application"

# -------------------------
# Database Configuration (PlanetScale)
# -------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME"),          # Database name
        "USER": os.environ.get("DB_USER"),          # Database user
        "PASSWORD": os.environ.get("DB_PASSWORD"),  # Database password
        "HOST": os.environ.get("DB_HOST"),          # Database host (PlanetScale URL)
        "PORT": os.environ.get("DB_PORT", 3306),    # Default MySQL port
        "OPTIONS": {
            "ssl": {
                "ssl-mode": "VERIFY_IDENTITY"      # Required for PlanetScale SSL
            }
        },
    }
}

# -------------------------
# Password Validators
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------
# Internationalization
# -------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

# -------------------------
# Static & Media
# -------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"   # <-- Add this for deployment

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"     # <-- Add this for deployment

# -------------------------
# Default Auto Field
# -------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
