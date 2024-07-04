from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.db import models
from autoslug import AutoSlugField
from django.core.validators import validate_comma_separated_integer_list
import os
from activity.models import ModuleActivity, LessonActivity

class LearningPath(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

def course_image_upload_to(instance, filename):
    return os.path.join( 'courses', str(instance.id), 'images', filename)

class Course(models.Model):
    DRAFT = 'draft'
    IN_REVIEW = 'in_review'
    PUBLISHED = 'published'

    CHOICES_STATUS = (
        (DRAFT, 'Draft'),
        (IN_REVIEW, 'In review'),
        (PUBLISHED, 'Published')
    )
    learning_path = models.ForeignKey(LearningPath, related_name='courses', on_delete=models.SET_NULL, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='courses')
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    short_description = models.TextField(blank=True, null=True)
    long_description =  models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_courses', on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField (upload_to=course_image_upload_to,blank=True, null=True)
    status =  models.CharField(max_length=20, choices=CHOICES_STATUS, default=DRAFT)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return 'https://imageplaceholder.net/960x905'

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    description = models.TextField(blank=True, null=True)
    is_open = models.BooleanField(default=False)

    def __str__(self):
        return self.title

def lesson_file_upload_to_file(instance, filename):
    return os.path.join( 'courses', str(instance.module.course.id),  str(instance.module.id), 'lessons', filename)

def lesson_file_upload_to_video(instance, filename):
    return os.path.join( 'courses',  str(instance.module.course.id), str(instance.module.id), 'lessons', filename)


class Lesson(models.Model):
    ARTICLE = 'article'
    QUIZ = 'quiz'
    VIDEO = 'video'
    FILE = 'file'
    
    LESSON_TYPES = (
        (ARTICLE, 'Article'),
        (QUIZ, 'Quiz'),
        (VIDEO, 'Video'),
        (FILE, 'File'),
    )

    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default=ARTICLE)
    video = models.FileField(upload_to=lesson_file_upload_to_video, blank=True, null=True)
    youtube_id = models.CharField(max_length=30, blank=True, null=True)
    file = models.FileField(upload_to=lesson_file_upload_to_file, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_file(self):
        if self.file and self.file.url:
            return settings.WEBSITE_URL + self.file.url
        return None
    
    def get_video(self):
        if self.video and self.video.url:
            return settings.WEBSITE_URL + self.video.url
        return None

class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lesson_comments', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='lesson_commentor',
          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Comment lesson: {self.lesson} by user: {self.created_by}"

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"For: {self.user}, Course: {self.course}"

class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='progresses', on_delete=models.CASCADE)
    completed_modules = models.PositiveIntegerField(default=0)
    total_modules = models.PositiveIntegerField(default=0)
    completed_lessons = models.PositiveIntegerField(default=0)
    total_lessons = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"For: {self.user}, Course: {self.course}"

    @property
    def progress_percentage(self):
        total_activities = self.total_modules + self.total_lessons
        completed_activities = self.completed_modules + self.completed_lessons
        return (completed_activities / total_activities) * 100 if total_activities > 0 else 0

    def update_progress(self):
        from django.apps import apps
        ModuleActivity = apps.get_model('activity', 'ModuleActivity')
        LessonActivity = apps.get_model('activity', 'LessonActivity')
        
        self.total_modules = Module.objects.filter(course=self.course).count()
        self.total_lessons = Lesson.objects.filter(module__course=self.course).count()

        # Count completed lessons
        self.completed_lessons = LessonActivity.objects.filter(
            lesson__module__course=self.course, status=LessonActivity.DONE, created_by=self.user
        ).count()

        # Count completed modules
        completed_modules = 0
        modules = Module.objects.filter(course=self.course)
        for module in modules:
            lessons = Lesson.objects.filter(module=module)
            completed_lessons_in_module = LessonActivity.objects.filter(
                lesson__in=lessons, status=LessonActivity.DONE, created_by=self.user
            ).count()
            if completed_lessons_in_module == lessons.count():
                completed_modules += 1

        self.completed_modules = completed_modules

        self.save()