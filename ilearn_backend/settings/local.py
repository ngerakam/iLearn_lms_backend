from .base import *
import os

ALLOWED_HOSTS = ['0.0.0.0','*']

WEBSITE_URL = 'http://127.0.0.1:8000'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "../") + "db.sqlite3",
    }
}



EMAIL_HOST='localhost'
EMAIL_PORT=2525
