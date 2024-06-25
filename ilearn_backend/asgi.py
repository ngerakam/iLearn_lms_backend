"""
ASGI config for ilearn_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from ilearn_backend.settings.base import DEBUG

from django.core.asgi import get_asgi_application

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ilearn_backend.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ilearn_backend.settings.prod')

application = get_asgi_application()
