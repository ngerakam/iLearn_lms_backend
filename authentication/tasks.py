# tasks.py
from celery import shared_task
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import User, UserProfile
from .utils import (generate_random_password,
                                  get_default_from_email, get_site_contacts, send_html_email)


@shared_task
def assign_user_to_group(user_id):
    user = User.objects.get(id=user_id)
    if user.is_admin:
        group_name = 'admin'
    elif user.is_teacher:
        group_name = 'teacher'
    elif user.is_student:
        group_name = 'student'
    else:
        group_name = None

    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

@shared_task
def send_user_registration_email(user_id):
    user = User.objects.get(id=user_id)
    allowed_origin = settings.CORS_ALLOWED_ORIGINS[0]
    contacts = get_site_contacts()
    password = generate_random_password()

    # Determine the user role and select the appropriate email template
    if user.is_admin:
        template_name = 'authentication/user_registration_email_admin.html'
        subject = 'Welcome, Admin!'
    elif user.is_teacher:
        template_name = 'authentication/user_registration_email_teacher.html'
        subject = 'Welcome, Teacher!'
    elif user.is_student:
        template_name = 'authentication/user_registration_email_student.html'
        subject = 'Welcome, Student!'
    else:
        template_name = 'authentication/user_registration_email.html'
        subject = 'Welcome to Our Platform!'

    context = {
        'user': user,
        'url': allowed_origin,
        'contacts': contacts,
        'password': password
    }

    # Use the send_html_email utility to send the email
    send_html_email(subject, [user.email], template_name, context)

    # Set a generated password.
    user.password = make_password(password)
    user.save(update_fields=['password'])

    #for the manager python manage.py createsuperuser
    if user.is_superuser:
        userprofile = UserProfile.objects.get_or_create(user=user)