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
from .serializers import ModuleWithLessonsSerializer as CustomModuleSerializer
from .serializers import LessonSerializer as CustomLessonSerializer

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
            completions_per_course = CourseActivity.objects.filter(
                status='done',  # Assuming 'DONE' is the correct status string
                activity_course__created_by=request.user
            ).values('activity_course').annotate(
                total_completions=Count('created_by', distinct=True)
            )
            
            # Prepare response data
            response_data = []
            for completion in completions_per_course:
                course = Course.objects.get(pk=completion['activity_course'])
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


class CourseCompletionActivitiesView(APIView):
    def get(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            modules = course.modules.all()
            
            user_ids = CourseActivity.objects.filter(activity_course=course).values_list('created_by_id', flat=True).distinct()
            
            module_data = []

            for module in modules:
                lessons = module.lessons.all()
                completed_users_count = 0
                lessons_data = []

                for lesson in lessons:
                    completed_users = LessonActivity.objects.filter(
                        activity_lesson=lesson,
                        status='done'
                    ).values('created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_at').distinct()

                    lessons_data.append({
                        'id': lesson.id,
                        'title': lesson.title,
                        'completed_users': list(completed_users),
                    })
                    
                    completed_users_count += completed_users.count()
                
                module_data.append({
                    'id': module.id,
                    'title': module.title,
                    'completed_users_count': completed_users_count,
                    'lessons': lessons_data,
                })

            # Check if all modules and lessons are completed by each user
            for user_id in user_ids:
                user = User.objects.get(pk=user_id)
                all_modules_completed = True
                
                for module in modules:
                    lessons = module.lessons.all()
                    all_lessons_completed = all(
                        LessonActivity.objects.filter(
                            activity_lesson=lesson,
                            status='done',
                            created_by=user
                        ).exists() for lesson in lessons
                    )
                    
                    if all_lessons_completed:
                        ModuleActivity.objects.update_or_create(
                            activity_module=module,
                            created_by=user,
                            defaults={'status': 'done'}
                        )
                    else:
                        ModuleActivity.objects.update_or_create(
                            activity_module=module,
                            created_by=user,
                            defaults={'status': 'started'}
                        )
                        all_modules_completed = False
                
                if all_modules_completed:
                    CourseActivity.objects.update_or_create(
                        activity_course=course,
                        created_by=user,
                        defaults={'status': 'done'}
                    )
                else:
                    CourseActivity.objects.update_or_create(
                        activity_course=course,
                        created_by=user,
                        defaults={'status': 'started'}
                    )

            return Response({
                'course': {
                    'id': course.id,
                    'title': course.title,
                    'short_description': course.short_description,
                    'get_image': course.get_image(),
                    'modules': module_data,
                }
            }, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CourseActivitiesView(APIView):
    def get(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            modules = course.modules.all()
            
            module_data = []

            for module in modules:
                lessons = module.lessons.all()
                lessons_data = []

                for lesson in lessons:
                    lesson_activities = LessonActivity.objects.filter(activity_lesson=lesson)
                    completed_users = lesson_activities.filter(status='done').values(
                        'created_by__id', 'created_by__first_name', 'created_by__last_name', 'created_at'
                    ).distinct()

                    lessons_data.append({
                        'id': lesson.id,
                        'title': lesson.title,
                        'completed_users': list(completed_users),
                        'status': lesson_activities.values('status').first()['status'] if lesson_activities.exists() else None
                    })
                
                module_status = ModuleActivity.objects.filter(activity_module=module).values('status').first()
                module_data.append({
                    'id': module.id,
                    'title': module.title,
                    'completed_users_count': sum(1 for lesson in lessons_data if lesson['status'] == 'done'),
                    'lessons': lessons_data,
                    'status': module_status['status'] if module_status else None
                })

            course_status = CourseActivity.objects.filter(activity_course=course).values('status').first()

            return Response({
                'course': {
                    'id': course.id,
                    'title': course.title,
                    'short_description': course.short_description,
                    'get_image': course.get_image(),
                    'modules': module_data,
                    'status': course_status['status'] if course_status else None
                }
            }, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)