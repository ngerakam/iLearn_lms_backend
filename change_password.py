"""""

This file is for changing of superuser's password via the terminal

Usage : python change_password.py <email> <new_password>

"""

import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model

def set_django_settings():
    # Determine the appropriate settings module based on DEBUG
    settings_module = "ilearn_backend.settings.local" if settings.configured and settings.DEBUG else "ilearn_backend.settings.prod"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    django.setup()

def change_user_password(email, new_password):
    User = get_user_model()  # This will use the custom User model from your authentication app
    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)  # Ensure your User model uses set_password to hash the password
        user.save()
        print(f"Password for user with email '{email}' has been changed successfully.")
    except User.DoesNotExist:
        print(f"User with email '{email}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import argparse

    # Set up Django environment
    set_django_settings()

    parser = argparse.ArgumentParser(description='Change a user\'s password.')
    parser.add_argument('email', type=str, help='The email of the user whose password you want to change.')
    parser.add_argument('new_password', type=str, help='The new password for the user.')

    args = parser.parse_args()

    change_user_password(args.email, args.new_password)
