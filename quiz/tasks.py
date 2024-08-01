import logging
from celery import shared_task
from .utils import run_calculate_quiz_score

logger = logging.getLogger(__name__)

@shared_task
def calculate_quiz_score(attempt_id):
  run_calculate_quiz_score(attempt_id)