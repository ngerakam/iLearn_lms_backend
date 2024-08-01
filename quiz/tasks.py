from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.utils import timezone
from .utils import run_calculate_quiz_score

@shared_task
def calculate_quiz_score(attempt_id):
    run_calculate_quiz_score(attempt_id)