from rest_framework import serializers

from authentication.models import User
from course.models import Course, Module, Lesson

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email' ]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description','long_description','get_image')

class ModuleSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False)
    class Meta:
        model = Module
        fields = ('id', 'course', 'title', 'slug', 'description')

class LessonSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(many=False)
    class Meta:
        model = Lesson
        fields = ('id', 'module', 'title', 'slug', 'short_description')

class ModuleWithLessonsSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    course = CourseSerializer(many=False)

    class Meta:
        model = Module
        fields = ('id', 'course', 'title', 'slug', 'description', 'lessons')