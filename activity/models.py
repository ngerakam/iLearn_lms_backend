# from django.contrib.auth.models import User
from django.db import models

from course.models import Course, Lesson,Quiz

from authentication.models import User

class Activity(models.Model):
    STARTED ='started'
    DONE = 'done'

    STATUS_CHOICES = (
        (STARTED,'Started'),
        (DONE,'Done')
    )

    course = models.ForeignKey(Course, related_name='activities', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='activities', on_delete=models.CASCADE)
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default=STARTED)
    created_by = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"For: {self.created_by}, Course: {self.course}, Lesson: {self.lesson}, Status: {self.status}"

class CourseStatus(models.Model):
    STARTED ='started'
    DONE = 'done'

    STATUS_CHOICES = (
        (STARTED,'Started'),
        (DONE,'Done')
    )

    course = models.ForeignKey(Course, related_name='course_statuses', on_delete=models.CASCADE)
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default=STARTED)
    created_by = models.ForeignKey(User, related_name='course_statuses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Course: {self.course}, User: {self.created_by}, Status: {self.status}"

class ScoreBoard(models.Model):
    course = models.ForeignKey(Course, related_name='scores', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='scores', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='scores', on_delete=models.CASCADE)
    created_by = created_by = models.ForeignKey(User, related_name='scores', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = 'Scores'
    
    def __str__(self):
        return f"For: {self.created_by}, Course: {self.course}, Lesson: {self.lesson}, Quiz: {self.quiz}"
    
class Enrollment(models.Model):
    created_by = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Enrollments'
    
    def __str__(self):
        return f"{self.created_by} has enrolled to: {self.course}"