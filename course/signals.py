from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment
from .tasks import send_course_enrollment_email

@receiver(post_save, sender=Enrollment)
def create_progress_signal(sender, instance, created, **kwargs):
    user = instance.user.id
    course = instance.course.id
    if created:
        send_course_enrollment_email.delay(user,course)

