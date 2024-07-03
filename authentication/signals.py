from django.contrib.auth.models import Group
from .models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New user created: {instance.email}")

    if instance.is_admin:
        group_name = 'admin'
    elif instance.is_teacher:
        group_name = 'teacher'
    elif instance.is_student:
        group_name = 'student'
    else:
        group_name = None

    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)
        logger.info(f"User {instance.email} added to group: {group_name}")
