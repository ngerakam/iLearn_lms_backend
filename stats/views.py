from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from activity.models import CourseActivity, ModuleActivity, LessonActivity
from activity.serializers import (CourseActivitySerializer,
                                   ModuleActivitySerializer, LessonActivitySerializer)
from authentication.models import User
from course.models import Course, Module, Lesson, Enrollment
from course.serializers import (CourseSerializer, ModuleSerializer, LessonSerializer,
                                EnrollmentSerializer)

class EnrollmentCountView(APIView):
    def get(self, request):
        try:
            enrollments_per_course = Enrollment.objects.filter(
                course__created_by_id=request.user.id).values('course'
                                                              ).annotate(
                                                                  total_enrollments=Count('id'))
            response_data = []
            for enrollment in enrollments_per_course:
                course = Course.objects.get(pk=enrollment['course'])
                data = {
                    'course_id': course.id,
                    'course_title': course.title,
                    'total_enrollments': enrollment['total_enrollments']
                }
                response_data.append(data)
            
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompletionStatusView(APIView):
    def get(self, request):
        try:
            # Count number of users who have completed each course created by the authenticated user
            completions_per_course = CourseActivity.objects.filter(status='done'
                                                                   , activity_course__created_by_id=request.user.id
                                                                   ).values('activity_course').annotate(
                                                                       total_completions=Count('id'))
            
            # Prepare response data
            response_data = []
            for completion in completions_per_course:
                course = Course.objects.get(pk=completion['course'])
                data = {
                    'course_id': course.id,
                    'course_title': course.title,
                    'total_completions': completion['total_completions']
                }
                response_data.append(data)
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TotalUserCourses(APIView):
    def get(self, request):
        try:
            #Count the number of courses that a user has
            total_courses = Course.objects.filter(created_by=request.user).count()
            return Response({
                "total_courses": total_courses,
                "status": status.HTTP_200_OK
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CourseActivityAPIView(APIView):
    def get(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            activity = CourseActivity.objects.filter(
                activity_course=course,created_by=request.user)
            serializer = CourseActivitySerializer(activity, many=False)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ModuleActivityAPIView(APIView):
    def get(self, request, mod_slug):
        try:
            module = Module.objects.get(slug=mod_slug)
            activity = ModuleActivity.objects.filter(
                activity_module=module,created_by=request.user)
            serializer = ModuleActivitySerializer(activity, many=False)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LessonActivityAPIView(APIView):
    def get(self, request, lesson_slug):
        try:
            lesson = Lesson.objects.get(slug=lesson_slug)
            activity = LessonActivity.objects.filter(
                activity_lesson=lesson,created_by=request.user)
            serializer = LessonActivitySerializer(activity, many=False)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)