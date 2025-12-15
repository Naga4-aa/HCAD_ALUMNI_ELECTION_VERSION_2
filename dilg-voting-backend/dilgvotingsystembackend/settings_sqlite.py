from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Enable debug locally so Django serves admin static assets.
DEBUG = True
