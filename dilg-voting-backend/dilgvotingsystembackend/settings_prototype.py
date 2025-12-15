"""
Hardened settings for local prototype demos.
Keeps the running site untouched while showcasing better defaults.
"""

import os

from .settings import *  # noqa: F401,F403

# Require secrets from environment instead of hardcoding.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# Restrict hosts and CORS to expected domains; override via env for demos.
ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "hcadalumni.org,www.hcadalumni.org,localhost,127.0.0.1",
).split(",")

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://hcadalumni.org",
    "https://www.hcadalumni.org",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# CSRF and transport security for HTTPS.
CSRF_TRUSTED_ORIGINS = [
    "https://hcadalumni.org",
    "https://www.hcadalumni.org",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv("DJANGO_FORCE_SSL", "True").lower() == "true" and not DEBUG
SECURE_HSTS_SECONDS = 0 if DEBUG else 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_REFERRER_POLICY = "same-origin"

# Stronger password policy for the prototype.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Database: require env-provided credentials; prefer TLS if supported.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("MYSQL_DATABASE", ""),
        "USER": os.environ.get("MYSQL_USER", ""),
        "PASSWORD": os.environ.get("MYSQL_PASSWORD", ""),
        "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {
            "ssl": {"ssl-mode": "REQUIRED"},
        },
    }
}

# Light throttling to demonstrate brute-force protection.
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": os.getenv("DRF_USER_RATE", "100/hour"),
        "anon": os.getenv("DRF_ANON_RATE", "20/hour"),
    },
}
