import string, secrets
from .models import SiteAddress
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

def get_default_from_email():
    try:
        site_address = SiteAddress.objects.first()
        if site_address:
            return site_address.email_contact
 
    except SiteAddress.DoesNotExist:
        if settings.EMAIL_HOST_USER:
            return settings.EMAIL_HOST_USER
        else:
            return 'iLearn@ilearn.com'  

def get_site_contacts():
    try:
        site_address = SiteAddress.objects.first()
        if site_address:
            return site_address
    except SiteAddress.DoesNotExist:
        return 'iLearn@ilearn.com'  


def send_email(user, subject, msg):
    send_mail(
        subject,
        msg,
        settings.EMAIL_FROM_ADDRESS,
        [user.email],
        fail_silently=False,
    )


def send_html_email(subject, recipient_list, template, context):
    """A function responsible for sending HTML email"""
    # Render the HTML template
    html_message = render_to_string(template, context)

    # Generate plain text version of the email (optional)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        html_message=html_message,
    )
