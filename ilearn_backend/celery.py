from __future__ import absolute_import, unicode_literals
import os
from dotenv import load_dotenv

load_dotenv()
from celery import Celery

# Set the default Django settings module for the 'celery' program.
# It's essential to determine the environment before any Django imports.
if os.environ.get('DEBUG', 'False') == 'True':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ilearn_backend.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ilearn_backend.settings.prod')

app = Celery('ilearn_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Set the broker connection retry on startup
app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
