import string, secrets
from .models import SiteAddress
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
