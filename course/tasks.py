# tasks.py
from django.conf import settings
from celery import shared_task
from .models import Enrollment, Progress, Course
from activity.models import CourseActivity
from authentication.utils import (generate_random_password,
                                  get_default_from_email, get_site_contacts, send_html_email)
from authentication.models import User


@shared_task
def create_progress(enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    Progress.objects.create(user=enrollment.user, course=enrollment.course)
    CourseActivity.objects.create(activity_course=enrollment.course,
                                  status='started', created_by=enrollment.user)

@shared_task
def send_course_enrollment_email(user_id,course_id):
    user = User.objects.get(id=user_id)
    allowed_origin = settings.CORS_ALLOWED_ORIGINS[0]
    contacts = get_site_contacts()
    course = Course.objects.get(id=course_id)
    template_name = 'course/course_registration_email.html'
    subject = 'Congratulations on Enrolling to our course!'

    context = {
        'user': user,
        'url': allowed_origin,
        'contacts': contacts,
        'course': course
    }

    send_html_email(subject, [user.email], template_name, context)