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

EMAIL_HOST='localhost'
EMAIL_PORT=2525