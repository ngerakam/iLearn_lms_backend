from datetime import datetime, timedelta
import random, string, os
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Sum



class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin= False
        user.is_staff= False
        user.is_student= False
        user.is_teacher = False
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin= True
        user.is_staff= True
        user.is_student= False
        user.is_teacher = False
        user.is_superuser= True
        user.save(using=self._db)
        return user
    
    def total_registered_users(self, user):
        return self.filter(registered_by=user).count()
        

class User(AbstractUser):
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    tfa_secret = models.CharField(max_length=255, default='',blank=True,null=True)
    registered_by = models.CharField(max_length=255,default='',blank=True,null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}, email: {self.email}"

def profile_image_upload_to(instance, filename):
    return os.path.join( 'profiles', str(instance.id), filename)
class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profle_image = models.ImageField (upload_to=profile_image_upload_to,blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='None')
    about_me = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def get_profile_image(self):
        if self.profle_image:
            return settings.WEBSITE_URL + self.profle_image.url
        else:
            return 'https://imageplaceholder.net/960x905'

def site_image_upload_to(instance, filename):
    return os.path.join( 'site', str(instance.id), 'config', filename)
class SiteSetup(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    card1_name = models.CharField(max_length=100, blank=True, null=True)
    card1 = models.TextField(blank=True, null=True)
    card2_name = models.CharField(max_length=100, blank=True, null=True)
    card2 = models.TextField(blank=True, null=True)
    card3_name = models.CharField(max_length=100, blank=True, null=True)
    card3 = models.TextField(blank=True, null=True)
    hero_name = models.CharField(max_length=100, blank=True, null=True)
    hero_message = models.TextField(blank=True, null=True)
    login_image = models.ImageField (upload_to=site_image_upload_to,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'SiteSetup'

    def __str__(self):
        return self.title

    def get_site_image(self):
        if self.login_image:
            return settings.WEBSITE_URL + self.login_image.url
        else:
            return 'https://imageplaceholder.net/960x905'
        
    def save(self, *args, **kwargs):
        if not self.pk and SiteSetup.objects.exists():
            raise ValidationError('There can be only one SiteSetup instance')
        return super(SiteSetup, self).save(*args, **kwargs)
    

class SiteAbout(models.Model):
    site = models.OneToOneField(SiteSetup,related_name='abouts', on_delete=models.CASCADE)
    about_message = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'SiteAbout'

    def __str__(self):
        return f"About for: {self.site}"
    
class SiteAddress(models.Model):
    site = models.OneToOneField(SiteSetup,related_name='addresses', on_delete=models.CASCADE)
    email_contact = models.CharField(max_length=250, blank=True, null=True)
    phone_contact = models.CharField(max_length=250, blank=True, null=True)
    location_address = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'SiteAddress'

    def __str__(self):
        return f"Adress for: {self.site}"