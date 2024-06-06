import os
from django.conf import settings
# from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

from authentication.models import User

from autoslug import AutoSlugField


def validate_file_extension(value):
    valid_extensions = ['.pdf', '.doc', '.docx', '.txt', '.pptx']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}')

def validate_video_extension(value):
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f'Unsupported video extension. Allowed extensions are: {", ".join(valid_extensions)}')


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    short_description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

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

    categories = models.ManyToManyField(Category,related_name='categories')
    title = models.CharField(max_length=255, default='')
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='courses',on_delete=models.CASCADE)
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

def lesson_file_upload_to_file(instance, filename):
    return os.path.join( 'courses', str(instance.course.id), 'lessons', str(instance.id),'document', filename)

def lesson_file_upload_to_video(instance, filename):
    return os.path.join( 'courses', str(instance.course.id), 'lessons', str(instance.id),'video', filename)

class Lesson(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'

    CHOICES_STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    ARTICLE = 'article'
    QUIZ = 'quiz'
    VIDEO = 'video'
    File = 'file'

    CHOICES_LESSON_TYPE = (
        (ARTICLE, 'Article'),
        (QUIZ, 'Quiz'),
        (VIDEO, 'Video'),
        (File, 'File')
    )

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    status =  models.CharField(max_length=20, choices=CHOICES_STATUS, default=DRAFT)
    lesson_type = models.CharField(max_length=20, choices=CHOICES_LESSON_TYPE, default=ARTICLE)
    video = models.FileField(upload_to=lesson_file_upload_to_video, blank=True, null=True, validators=[validate_video_extension])
    youtube_id  = models.CharField(max_length=30, blank=True, null=True)
    file = models.FileField(upload_to=lesson_file_upload_to_file, blank=True, null=True, validators=[validate_file_extension])

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
    course = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f"course: {self.course} in lesson: {self.lesson} by user: {self.created_by}"

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    question = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return f"{self.question} Quiz for: {self.lesson} lesson"