from django.db.models import Q

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import (CourseActivity,ModuleActivity,LessonActivity,
                     ActivityLog)
from .serializers import (CourseActivitySerializer, ModuleActivitySerializer,
                          LessonActivitySerializer, ActivityLogSerializer)

from course.models import (Course, Module, Lesson, Enrollment)

from course.serializers import (CourseSerializer, CourseStatusSerializer)

class CourseActivityListAPIView(APIView):
    def get(self, request):
        try:
            activities = CourseActivity.objects.filter(created_by=request.user)
            serializer = CourseActivitySerializer(activities, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ModuleActivityListAPIView(APIView):
    def get(self, request):
        try:
            modules = ModuleActivity.objects.filter(created_by=request.user)
            serializer = ModuleActivitySerializer(modules, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        data = request.data
        try:
            module = Module.objects.get(slug=data.get('slug'))
            mda = ModuleActivity.objects.create(
                module = module,
                status = 'started',
                created_by = request.user
            )
            mda.save()
            serializer = ModuleActivitySerializer(mda, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LessonActivityListAPIView(APIView):
    def get(self, request):
        try:
            lessons = LessonActivity.objects.filter(created_by=request.user)
            serializer = LessonActivitySerializer(lessons, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        try:
            lesson = Lesson.objects.get(slug=data.get('slug'))
            lesson_activity = LessonActivity.objects.create(
                lesson = lesson,
                status = 'started',
                created_by = request.user
            )
            lesson_activity.save()
            serializer = LessonActivitySerializer(lesson_activity, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ActivityLogListAPIView(APIView):
    def get(self, request):
        try:
            activity_logs = ActivityLog.objects.all()
            serializer = ActivityLogSerializer(activity_logs, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



##############  Custome Views ##############################

class CreatedCoursesListAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            courses = user.created_courses.all()
            serializer = CourseStatusSerializer(courses, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UnpublishedCoursesListAPIView(APIView):
    def get(self, request):
        try:
            courses = Course.objects.filter(
            created_by=request.user).filter(Q(status=Course.DRAFT) | Q(status=Course.IN_REVIEW)
            )
            serializer = CourseStatusSerializer(courses, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompletedCoursesListAPIView(APIView):
    def get(self, request):
        try:
            activities = CourseActivity.objects.filter(created_by=request.user,
                                                       status='done')
            courses = [activity.course for activity in activities ]
            serializer = CourseSerializer(courses, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EnrolledCoursesListAPIView(APIView):
    def get(self, request):
        try:
            enrollments = Enrollment.objects.filter(user=request.user)
            courses = [enrollment.course for enrollment in enrollments]
            serializer = CourseSerializer(courses, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class FrontPageCoursesListAPIView(APIView):
    def get(self, request):
        try:
            courses = Course.objects.filter(status=Course.PUBLISHED)[0:4]
            serializer = CourseSerializer(courses, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)