from rest_framework import serializers

from .models import CourseActivity, ModuleActivity, LessonActivity, ActivityLog

class CourseActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseActivity
        fields = ('id','course', 'status', 'created_by')

class ModuleActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleActivity
        fields = ('id', 'module','status', 'created_by')

class LessonActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonActivity
        fields = ('id', 'lesson','status', 'created_by')

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ('id', 'message', 'created_at')