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

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 25))  # Default to port 25 if not specified
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == 'True'  # Convert string to boolean
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == 'True'  # Convert string to boolean
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")