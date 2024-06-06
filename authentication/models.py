from datetime import datetime, timedelta
import random, string
from django.dispatch import receiver
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

class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='None')