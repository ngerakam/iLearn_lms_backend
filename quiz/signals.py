from datetime import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EssayGrade, EssayQuestionAnswer
from .tasks import run_calculate_quiz_score

@receiver(post_save, sender=EssayGrade)
def regrade_essay(sender, instance, created, **kwargs):
    if not created and instance.score is not None:
        run_calculate_quiz_score.delay(instance.quiz_attempt.id)


@receiver(post_save, sender=EssayGrade)
def update_quiz_score(sender, instance, **kwargs):
    if instance.grader and instance.score is not None:
        # Update the graded_at field
        instance.graded_at = timezone.now()
        instance.save(update_fields=['graded_at'])

        # Check if all essays are graded
        if instance.quiz_attempt.all_essays_graded():
            instance.quiz_attempt.score_calculated = False
            instance.quiz_attempt.save()
            run_calculate_quiz_score.delay(instance.quiz_attempt.id)