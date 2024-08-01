from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EssayGrade
from .tasks import calculate_quiz_score

@receiver(post_save, sender=EssayGrade)
def regrade_essay(sender, instance, created, **kwargs):
    if not created and instance.score is not None:
        calculate_quiz_score.delay(instance.quiz_attempt.id)