from .base import *


ALLOWED_HOSTS = ['0.0.0.0','*']

WEBSITE_URL = 'http://192.0.0.18:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mgfoundation',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': 'Chipskuku@1',
        'PORT': '3306'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_host'
EMAIL_PORT = 'your_smtp_port'
EMAIL_USE_TLS = True  # Or False if not using TLS
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'