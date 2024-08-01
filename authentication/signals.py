# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import assign_user_to_group, send_user_registration_email
from .models import User

@receiver(post_save, sender=User)
def assign_user_to_group_signal(sender, instance, created, **kwargs):
    if created:
        assign_user_to_group.delay(instance.id)

@receiver(post_save, sender=User)
def send_user_registration_email_signal(sender, instance, created, **kwargs):
    if created:
        send_user_registration_email.delay(instance.id)