from rest_framework import serializers

from .models import CourseActivity, ModuleActivity, LessonActivity, ActivityLog

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

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ('id', 'message', 'created_at')