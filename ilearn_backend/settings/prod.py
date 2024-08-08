from .base import *


ALLOWED_HOSTS = ['0.0.0.0','*']


DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

import os

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == 'True'
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == 'True'

if EMAIL_USE_SSL:
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
    EMAIL_USE_TLS = False  # Ensure TLS is not used if SSL is enabled
elif EMAIL_USE_TLS:
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USE_SSL = False  # Ensure SSL is not used if TLS is enabled
else:
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 25))
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = False

# Make sure EMAIL_USE_TLS or EMAIL_USE_SSL is set correctly
if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ValueError('EMAIL_USE_TLS and EMAIL_USE_SSL are mutually exclusive; only one should be True.')

# Set Django email settings
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 25))
