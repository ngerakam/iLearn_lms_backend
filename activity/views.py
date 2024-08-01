from django.db.models import Q

from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import (CourseActivity,ModuleActivity,LessonActivity,
                     ActivityLog)
from .serializers import (CourseActivitySerializer, ModuleActivitySerializer,
                          LessonActivitySerializer, ActivityLogSerializer)

from course.tasks import send_course_completion_email

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
                activity_module = module,
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
                activity_lesson = lesson,
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



##############  Custom Views ##############################

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
            courses = [activity.activity_course for activity in activities ]
            serializer = CourseSerializer(courses, many=True)

            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EnrolledCoursesListAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            enrollments = Enrollment.objects.filter(user=user).select_related('course')
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


class CourseActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            # print("Course ",course)
            activity = CourseActivity.objects.get(
                activity_course_id=course.id,
                created_by_id=request.user.id)
            # print("Activity ",activity)
            serializer = CourseActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except CourseActivity.DoesNotExist:
            return Response(
                {'error': 'Course activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, course_slug):
        # print(request.data)
        try:
            course = Course.objects.get(slug=course_slug)
            activity = CourseActivity.objects.get(
                activity_course_id=course.id,
                created_by_id=request.user.id)
            activity.status=request.data.get('status')
            activity.save()
            send_course_completion_email(request.user.id, course.id)
            serializer = CourseActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except CourseActivity.DoesNotExist:
            return Response(
                {'error': 'Course activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ModuleActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, mod_slug):
        try:
            module = Module.objects.get(slug=mod_slug)
            activity = ModuleActivity.objects.get(
                activity_module_id=module.id,
                created_by_id=request.user.id)
            serializer = ModuleActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except ModuleActivity.DoesNotExist:
            return Response(
                {'error': 'Module activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, mod_slug):
        try:
            module = Module.objects.get(slug=mod_slug)
            activity = ModuleActivity.objects.get(
                activity_module_id=module.id,
                created_by_id=request.user.id)
            activity.status = request.data.get('status')
            activity.save()
            serializer = ModuleActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except ModuleActivity.DoesNotExist:
            return Response(
                {'error': 'Module activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, mod_slug):
        try:
            module = Module.objects.get(slug=mod_slug)
            activity = ModuleActivity.objects.create(
                activity_module = module,
                created_by = request.user,
                status = "started"
            )
            activity.save()
            serializer = ModuleActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except ModuleActivity.DoesNotExist:
            return Response(
                {'error': 'Module activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            

class LessonActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, lesson_slug):
        try:
            lesson = Lesson.objects.get(slug=lesson_slug)
            activity = LessonActivity.objects.get(
                activity_lesson_id=lesson.id,
                created_by_id=request.user.id)
            serializer = LessonActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except LessonActivity.DoesNotExist:
            return Response(
                {'error': 'Lesson activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, lesson_slug):
        try:
            lesson = Lesson.objects.get(slug=lesson_slug)
            activity = LessonActivity.objects.get(
                activity_lesson_id=lesson.id,
                created_by_id=request.user.id)
            activity.status = request.data.get('status')
            activity.save()
            serializer = LessonActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except LessonActivity.DoesNotExist:
            return Response(
                {'error': 'Lesson activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, lesson_slug):
        try:
            lesson = Lesson.objects.get(slug=lesson_slug)
            activity = LessonActivity.objects.create(
                activity_lesson = lesson,
                created_by = request.user,
                status = "started"
            )
            activity.save()                
            serializer = LessonActivitySerializer(activity, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except LessonActivity.DoesNotExist:
            return Response(
                {'error': 'Lesson activity not found for this user and course'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            





# ############## Function Based Views ######################
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_course_activity(request,course_slug):
#     try:
#         course = Course.objects.get(slug=course_slug)
#         print("Course ",course)
#         activity = CourseActivity.objects.get(
#             activity_course_id=course.id,
#             created_by_id=request.user.id)
#         print("Activity ",activity)
#         serializer = CourseActivitySerializer(activity, many=False)
#         return Response({"data":serializer.data}, status=status.HTTP_200_OK)
#     except CourseActivity.DoesNotExist:
#         return Response(
#             {'error': 'Course activity not found for this user and course'},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_module_activity(request,mod_slug):
#     try:
#         module = Module.objects.get(slug=mod_slug)
#         activity = ModuleActivity.objects.get(
#             activity_module_id=module.id,
#             created_by_id=request.user.id)
#         serializer = ModuleActivitySerializer(activity, many=False)
#         return Response({"data":serializer.data}, status=status.HTTP_200_OK)
#     except ModuleActivity.DoesNotExist:
#         return Response(
#             {'error': 'Module activity not found for this user and course'},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_lesson_activity(request,lesson_slug):
#     try:
#         lesson = Lesson.objects.get(slug=lesson_slug)
#         activity = LessonActivity.objects.get(
#             activity_lesson_id=lesson.id,
#              created_by_id=request.user.id)
#         serializer = LessonActivitySerializer(activity, many=False)
#         return Response({"data":serializer.data}, status=status.HTTP_200_OK)
#     except LessonActivity.DoesNotExist:
#         return Response(
#             {'error': 'Lesson activity not found for this user and course'},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)