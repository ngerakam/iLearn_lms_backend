from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, Progress

@receiver(post_save, sender=Enrollment)
def create_progress(sender, instance, created, **kwargs):
    if created:
        Progress.objects.create(user=instance.user, course=instance.course)