# tasks.py
from django.conf import settings
from celery import shared_task
from .models import Enrollment, Progress, Course
from activity.models import CourseActivity
from authentication.utils import (generate_random_password,
                                  get_default_from_email, get_site_contacts, send_html_email)
from authentication.models import User


@shared_task
def create_progress(user_id,course_id):
    user = User.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)
    Progress.objects.create(user=user, course=course)
    CourseActivity.objects.create(activity_course=course,
                                  status='started', created_by=user)

@shared_task
def send_course_enrollment_email(user_id,course_id):
    user = User.objects.get(id=user_id)
    allowed_origin = settings.CORS_ALLOWED_ORIGINS[0]
    contacts = get_site_contacts()
    course = Course.objects.get(id=course_id)
    template_name = 'course/course_registration_email.html'
    subject = f"Congratulations on Enrolling to our course {course.title} !"

    context = {
        'user': user,
        'url': allowed_origin,
        'contacts': contacts,
        'course': course
    }

    send_html_email(subject, [user.email], template_name, context)

@shared_task
def send_course_completion_email(user_id,course_id):
    user = User.objects.get(id=user_id)
    allowed_origin = settings.CORS_ALLOWED_ORIGINS[0]
    contacts = get_site_contacts()
    course = Course.objects.get(id=course_id)
    template_name = 'course/course_completion_email.html'
    subject = f"Congratulations on Completing the Course {course.title}!"

    context = {
        'user': user,
        'url': allowed_origin,
        'contacts': contacts,
        'course': course
    }

    send_html_email(subject, [user.email], template_name, context)