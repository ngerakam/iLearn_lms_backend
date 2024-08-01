from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EssayGrade, EssayQuestionAnswer
from .tasks import calculate_quiz_score

@receiver(post_save, sender=EssayGrade)
def regrade_essay(sender, instance, created, **kwargs):
    if not created and instance.score is not None:
        calculate_quiz_score.delay(instance.quiz_attempt.id)


@receiver(post_save, sender=EssayGrade)
def recalculate_quiz_score_on_essay_grade_update(sender, instance, **kwargs):
    if not kwargs.get('created') and instance.score is not None:
        instance.quiz_attempt.score_calculated = False
        instance.quiz_attempt.save(update_fields=['score_calculated'])
        calculate_quiz_score.apply_async(countdown=10, args=[instance.quiz_attempt.id])