from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from activity.models import Enrollment, CourseStatus, Activity
from course.models import Course,Lesson
from authentication.models import User
from .serializers import ActivitySerializer, CourseSerializer, LessonSerializer, CourseStatusSerializer

class EnrollmentCountView(APIView):
    def get(self, request):
        try:
            # Count number of enrollments per course created by the authenticated user
            enrollments_per_course = Enrollment.objects.filter(course__created_by_id=request.user.id).values('course').annotate(total_enrollments=Count('id'))
            
            # Prepare response data
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
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompletionStatusView(APIView):
    def get(self, request):
        try:
            # Count number of users who have completed each course created by the authenticated user
            completions_per_course = CourseStatus.objects.filter(status='done', course__created_by_id=request.user.id).values('course').annotate(total_completions=Count('id'))
            
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
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseActivitiesView(APIView):
    def get(self, request, pk=None):
        try:
            # Get course activities
            course = Course.objects.get(pk=pk)
            activities = course.activities.all()
            
            # Serialize data
            course_serializer = CourseSerializer(course)
            activities_serializer = ActivitySerializer(activities, many=True)

            return Response({
                "course": course_serializer.data,
                "activities": activities_serializer.data,
            }, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseCompleteionActivitiesView(APIView):
    def get(self, request, pk=None):
        try:
            # Get the course
            course = Course.objects.get(pk=pk)
            lessons = course.lessons.all()

            # Get all unique users from CourseStatus related to the course
            user_ids = CourseStatus.objects.filter(course=course).values_list('created_by_id', flat=True).distinct()

            completed_users = []

            # Check each user
            for user_id in user_ids:
                user = User.objects.get(pk=user_id)
                all_lessons_completed = all(
                    Activity.objects.filter(
                        course=course,
                        lesson=lesson,
                        status=Activity.DONE,
                        created_by=user
                    ).exists() for lesson in lessons
                )

                # Update or create CourseStatus based on lessons completion
                if all_lessons_completed:
                    completed_users.append(user)
                    CourseStatus.objects.update_or_create(
                        course=course,
                        created_by=user,
                        defaults={'status': CourseStatus.DONE}
                    )
                else:
                    CourseStatus.objects.update_or_create(
                        course=course,
                        created_by=user,
                        defaults={'status': CourseStatus.STARTED}
                    )

            # Get completed course statuses
            completed_course_statuses = CourseStatus.objects.filter(course=course, status=CourseStatus.DONE)

            completed_serializer = CourseStatusSerializer(completed_course_statuses, many=True)

            return Response({
                "completed_courses": completed_serializer.data,
            }, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)