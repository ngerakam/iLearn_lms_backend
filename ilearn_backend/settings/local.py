from .base import *
import os

ALLOWED_HOSTS = ['0.0.0.0','*']

WEBSITE_URL = os.getenv('WEBSITE_URL')


# Set X_FRAME_OPTIONS dynamically using the environment variable
X_FRAME_OPTIONS = f'ALLOW-FROM {WEBSITE_URL}'

CSP_FRAME_ANCESTORS = ("'self'", WEBSITE_URL)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "../") + "db.sqlite3",
    },
    'extras': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    },
}



EMAIL_HOST='localhost'
EMAIL_PORT=2525
