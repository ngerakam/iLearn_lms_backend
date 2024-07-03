from rest_framework import serializers
from authentication.models import User

from .models import (Course, Lesson, Comment, Category,
                     LearningPath, Enrollment, Module, Progress
                     )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name' )

class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = ('id','title', 'slug', 'description')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description','long_description','get_image')

class CourseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description','long_description','get_image', 'status',)

class CourseDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False)
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug',  'short_description','long_description', 'created_by')

class CourseDetailStatusSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug',  'short_description','long_description', 'created_by', 'status', 'categories')

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'title', 'slug', 'description','is_open')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'slug', 'lesson_type',
                   'short_description','long_description',
                   'get_video','youtube_id','get_file')

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False)
    class Meta:
        model = Comment
        fields = ('id', 'title', 'content', 'created_at', 'created_by')

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields= ('id','user','course','created_at')

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('id','user', 'course','completed_modules',
                 'total_modules','completed_lessons','total_lessons')