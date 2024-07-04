import time
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from .models import User, UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .utils import (generate_random_password,
                                  get_default_from_email, get_site_contacts)


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

@receiver(post_save, sender=User)
def send_user_registration_email(sender, instance, created, **kwargs):
    if created:
        allowed_origin = settings.CORS_ALLOWED_ORIGINS[0]
        contacts = get_site_contacts()
        password = generate_random_password()

        # Determine the user role and select the appropriate email template
        if instance.is_admin:
            template_name = 'authentication/user_registration_email_admin.html'
            subject = 'Welcome, Admin!'
        elif instance.is_teacher:
            template_name = 'authentication/user_registration_email_teacher.html'
            subject = 'Welcome, Teacher!'
        elif instance.is_student:
            template_name = 'authentication/user_registration_email_student.html'
            subject = 'Welcome, Student!'
        else:
            template_name = 'authentication/user_registration_email.html'
            subject = 'Welcome to Our Platform!'

        context = {
            'user': instance,
            'url': allowed_origin,
            'contacts': contacts,
            'password': password
        }

        html_message = render_to_string(template_name, context)
        send_mail(subject, None, get_default_from_email(), [instance.email], html_message=html_message)

        # Set a generated password.
        instance.password = make_password(password)
        instance.save(update_fields=['password'])

        #for the manager python manage.py createsuperuser
        if instance.is_superuser:
            userprofile = UserProfile.objects.get(user=instance)
            if userprofile:
                return
            else:
                UserProfile.objects.create(user=instance)