# utils.py
from authentication.models import SiteAddress

def get_default_from_email():
    try:
        site_address = SiteAddress.objects.first()
        if site_address:
            return site_address.email_contact
    except SiteAddress.DoesNotExist:
        return 'iLearn@ilearn.com'  

def get_site_contacts():
    try:
        site_address = SiteAddress.objects.first()
        if site_address:
            return site_address
    except SiteAddress.DoesNotExist:
        return 'iLearn@ilearn.com'  
