from rest_framework import serializers

from .models import Activity,ScoreBoard ,Enrollment, CourseStatus

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'course', 'lesson', 'status')

class CourseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'course', 'status')

class ScoreBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreBoard
        fields = ('id', 'course', 'lesson', 'quiz','score', 'created_by')

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('id', 'course', 'created_by')