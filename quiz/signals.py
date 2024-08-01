from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EssayGrade, EssayQuestionAnswer
# from .tasks import run_calculate_quiz_score
from .utils import run_calculate_quiz_score
from django.db import transaction


@receiver(post_save, sender=EssayGrade)
@transaction.atomic
def update_quiz_score(sender, instance, **kwargs):
    if instance.grader and instance.score is not None:
        instance.graded_at = datetime.now()

        # Check if all essays are graded
        if instance.quiz_attempt.all_essays_graded():
            instance.quiz_attempt.score_calculated = False
            instance.quiz_attempt.save()
            run_calculate_quiz_score(instance.quiz_attempt.id)