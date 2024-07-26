from rest_framework import serializers

from authentication.models import User
from course.models import Course, Module, Lesson
from activity.models import CourseActivity, ModuleActivity, LessonActivity, ActivityLog


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


class CourseActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseActivity
        fields = ('id','activity_course', 'status', 'created_by')

class ModuleActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleActivity
        fields = ('id', 'activity_module','status', 'created_by')

class LessonActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonActivity
        fields = ('id', 'activity_lesson','status', 'created_by')