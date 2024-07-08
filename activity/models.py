from django.db import models
from django.conf import settings
from django.apps import apps

STARTED ='started'
DONE = 'done'
NONE= 'none'

STATUS_CHOICES = (
    (STARTED,'Started'),
    (DONE,'Done'),
    (NONE, 'None')
)

class CourseActivity(models.Model):
    activity_course = models.ForeignKey('course.Course', related_name='course_activities', on_delete=models.CASCADE)
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default=NONE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'CourseActivities'
        unique_together = ('activity_course', 'created_by')

    def __str__(self):
        return f"For: {self.created_by}, Course: {self.activity_course}, Status: {self.status}"

class ModuleActivity(models.Model):
    activity_module = models.ForeignKey('course.Module', related_name='module_activities', on_delete=models.CASCADE)
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default=NONE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='module_activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'ModuleActivities'
        unique_together = ('activity_module', 'created_by')

    def __str__(self):
        return f"For: {self.created_by}, Course: {self.activity_module}, Status: {self.status}"

class LessonActivity(models.Model):
    activity_lesson = models.ForeignKey('course.Lesson', related_name='lesson_activities', on_delete=models.CASCADE)
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default=NONE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lesson_activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'LessonActivities'
        unique_together = ('activity_lesson', 'created_by')

    def __str__(self):
        return f"For: {self.created_by}, Lesson: {self.activity_lesson}, Status: {self.status}"


class ActivityLog(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.created_at}]{self.message}"
