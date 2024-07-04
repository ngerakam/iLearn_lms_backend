from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .utils import get_default_from_email, get_site_contacts, generate_random_password
from authentication.models import User
from course.models import Course
from django.shortcuts import get_object_or_404





# @receiver(post_save, sender=Enrollment)
# def send_course_enrollment_email(sender, instance, created, **kwargs):
#     if created:
#         allowed_origin = settings.CORS_ALLOWED_ORIGINS[0]
#         contacts = get_site_contacts()
#         user = instance.created_by
#         course = instance.course
#         context = {'user': user,
#                     'course': course,
#                     'url': allowed_origin,
#                     'contacts': contacts
#                     }
#         subject = f'You have enrolled in the course "{course.title}"'
#         html_message = render_to_string('notifications/course_enrollment_email.html',context )
#         send_mail(subject, None, get_default_from_email(), [user.email], html_message=html_message)


# @receiver(post_save, sender=CourseStatus)
# def send_course_completion_email(sender, instance, created, **kwargs):
#     if instance.status == CourseStatus.DONE and not created:  # Check status change to "Done"
#         user = instance.created_by
#         contacts = get_site_contacts()
#         course = instance.course
#         context ={'user': user,
#                 'course': course,
#                 'contacts': contacts}
#         subject = f'Congratulations on completing the course: {course.title}'
#         html_message = render_to_string('notifications/course_completion_email.html', context)
#         send_mail(subject, None, get_default_from_email(), [user.email], html_message=html_message)