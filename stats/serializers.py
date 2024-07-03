# from rest_framework import serializers

# from authentication.models import User
# from course.models import Course, Lesson
# from activity.models import  Enrollment, Activity,CourseStatus

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','first_name', 'last_name', 'email' ]

# class EnrollmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Enrollment
#         fields = ('id', 'course', 'created_by')

# class ActivitySerializer(serializers.ModelSerializer):
#     created_by = UserSerializer()
#     class Meta:
#         model = Activity
#         fields = '__all__'

# class LessonSerializer(serializers.ModelSerializer):
#     activities = ActivitySerializer(many=True, read_only=True)

#     class Meta:
#         model = Lesson
#         fields = ['id', 'title', 'activities', 'short_description']

# class CourseSerializer(serializers.ModelSerializer):
#     lessons = LessonSerializer(many=True, read_only=True)

#     class Meta:
#         model = Course
#         fields = ['id', 'title', 'lessons', 'short_description','get_image']

# class CourseStatusSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer()
#     course = CourseSerializer()
#     class Meta:
#         model = Activity
#         fields = ('id', 'course', 'status', 'created_by')