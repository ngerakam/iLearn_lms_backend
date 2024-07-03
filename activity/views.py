# from django.core.exceptions import ObjectDoesNotExist
# from django.shortcuts import get_object_or_404
# from django.db.models import Q

# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status

# from .models import Activity, Enrollment, ScoreBoard, CourseStatus
# from .serializers import ActivitySerializer, EnrollmentSerializer, CourseStatusSerializer

# from course.models import Course, Lesson, Quiz
# from course.serializers import CourseListSerializer,CourseListStatusSerializer

# @api_view(['GET'])
# def get_active_courses(request):
#     courses = []
#     activities = request.user.activities.all()

#     for activity in activities:
#         if activity.status == activity.STARTED and activity.course not in courses:
#             courses.append(activity.course)
#     serializer = CourseListSerializer(courses, many=True)

#     return Response(serializer.data)

# @api_view(['POST'])
# def course_track_started(request, course_slug):
#     course = Course.objects.get(slug=course_slug)

#     if CourseStatus.objects.filter(course=course
#                                    ,created_by=request.user
#                                 ).count() == 0:
#         CourseStatus.objects.create(course=course,
#                                     created_by=request.user
#                                 )
        
#     course_status =CourseStatus.objects.get(course=course,
#                                             created_by=request.user,
#                                 )
    
#     print(course_status)
    
#     serializer = CourseStatusSerializer(course_status)

#     return Response(serializer.data)

# @api_view(['POST'])
# def mark_course_done(request, course_slug):
#     course = Course.objects.get(slug=course_slug)

#     course_status =CourseStatus.objects.get(
#                                 course=course,
#                                 created_by=request.user
#                                 )
#     course_status.status = CourseStatus.DONE
#     course_status.save()
#     print(course_status)

#     serializer = CourseStatusSerializer(course_status)

#     return Response(serializer.data)

# @api_view(['GET'])
# def get_my_started_course(request, course_slug):
#     try:
#         course = Course.objects.get(slug=course_slug)
#         course_status = CourseStatus.objects.get(created_by_id=request.user.id, course=course)

#         if has_incomplete_activities(course, request.user):
#             course_status.status = CourseStatus.DONE
#             course_status.save()

#         serializer = CourseStatusSerializer(course_status)
#         return Response({
#             "course_status": serializer.data,
#             "message": "You have started this course",
#         }, status=status.HTTP_200_OK)

#     except Course.DoesNotExist:
#         return Response({
#             "message": "Course not found",
#         }, status=status.HTTP_404_NOT_FOUND)
#     except CourseStatus.DoesNotExist:
#         return Response({
#             "message": "You have not started this course",
#         }, status=status.HTTP_404_NOT_FOUND)

# def has_incomplete_activities(course, user):
#     return Activity.objects.filter(course=course, created_by=user).exclude(status=Activity.STARTED).exists()


# @api_view(['POST'])
# def track_started(request, course_slug,lesson_slug):
#     course = Course.objects.get(slug=course_slug)
#     lesson = Lesson.objects.get(slug=lesson_slug)

#     if Activity.objects.filter(created_by=request.user,
#                                 course=course, lesson=lesson).count() == 0:
#         Activity.objects.create(created_by=request.user,
#                                 course=course, lesson=lesson)
        
#     activity =Activity.objects.get(created_by=request.user,
#                                 course=course, lesson=lesson)
    
#     serializer = ActivitySerializer(activity)

#     return Response(serializer.data)

# @api_view(['POST'])
# def mark_done(request, course_slug,lesson_slug):
#     course = Course.objects.get(slug=course_slug)
#     lesson = Lesson.objects.get(slug=lesson_slug)

#     activity =Activity.objects.get(created_by=request.user,
#                                 course=course, lesson=lesson)
#     activity.status = Activity.DONE
#     activity.save()

#     serializer = ActivitySerializer(activity)

#     return Response(serializer.data)

# @api_view(['POST'])
# def create_score(request):
#     try:
#         scores = request.data  # Assuming request.data is a list of score objects

#         total_score = 0

#         for quiz_score in scores:
#             course = Course.objects.get(pk=quiz_score.get('course_id'))
#             lesson = Lesson.objects.get(pk=quiz_score.get('lesson_id'))
#             quiz = Quiz.objects.get(pk=quiz_score.get('quiz_id'))
#             score_entry = quiz_score.get('score_value')
#             score_value = int(quiz_score.get('score_value'))  # Convert score_value to integer

#             # Create ScoreBoard entry
#             score_entry = ScoreBoard.objects.create(
#                 course=course,
#                 lesson=lesson,
#                 quiz=quiz,
#                 score=score_entry,
#                 created_by=request.user
#             )

#             total_score += score_value  # Add score to total

#             score_entry.save()

#         return Response({
#             "total_score": total_score
#         })
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET'])
# def get_enrolled_courses(request):
#     enrollments = Enrollment.objects.filter(created_by=request.user)
#     courses = [enrollment.course for enrollment in enrollments]
#     serializer = CourseListSerializer(courses, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def get_my_enrolled_course(request, course_slug):
#     try:
#         course = Course.objects.get(slug=course_slug)
#         enrollment = Enrollment.objects.get(created_by=request.user, course=course)
#         serializer = EnrollmentSerializer(enrollment)
#         data = {
#             "enrollment": serializer.data,
#             "message": "You are enrolled",
#             "status": status.HTTP_200_OK
#         }
#         return Response(data)
#     except Course.DoesNotExist:
#         return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Enrollment.DoesNotExist:
#         return Response({"error": "You are not enrolled in this course"}, status=status.HTTP_403_FORBIDDEN)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def create_enrollment(request):
#     course_slug = request.data.get('course_slug')
#     user = request.user

#     if not course_slug:
#         return Response({"error": "Course slug is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         course = Course.objects.get(slug=course_slug)
#     except Course.DoesNotExist:
#         return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

#     # Check if the user is already enrolled
#     if Enrollment.objects.filter(created_by=user, course=course).exists():
#         return Response({"error": "You are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

#     # Create the enrollment
#     enrollment = Enrollment.objects.create(created_by=user, course=course)
#     serializer = EnrollmentSerializer(enrollment, many=False)
#     data = {
#         "enrollment": serializer.data,
#         "message": "Enrollment created successfully",
#          "status":status.HTTP_201_CREATED
#     }
#     return Response(data)

# @api_view(['GET'])
# def get_my_created_courses(request):
#     try:
#         courses = Course.objects.filter(
#                         created_by=request.user,)

#         serializer = CourseListStatusSerializer(
#             courses, many=True)
#         return Response(serializer.data)

#     except Exception as e:
#         return Response({
#             "message": str(e),
#         }, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])
# def get_my_unpublished_courses(request):
#     try:
#         courses = Course.objects.filter(
#             created_by=request.user).filter(Q(status=Course.DRAFT) | Q(status=Course.IN_REVIEW))
#         serializer = CourseListStatusSerializer(courses, many=True)
#         return Response(serializer.data)

#     except Exception as e:
#         return Response({
#             "message": str(e),
#         }, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET'])
# def get_my_completed_courses(request):
#     try:
#         courses_status = CourseStatus.objects.filter(created_by=request.user, status=CourseStatus.DONE)
#         courses = []
#         for status in courses_status:
#             try:
#                 course = Course.objects.get(pk=status.course_id)
#                 courses.append(course)
#             except Course.DoesNotExist:
#                 continue  # Skip this CourseStatus if the corresponding Course does not exist

#         serializer = CourseListSerializer(courses, many=True)
#         return Response(serializer.data)
#     except Exception as e:
#         return Response({
#             "message": str(e),
#         }, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET'])
# def get_my_registered_courses(request):
#     try:
#         # Get all enrollments for the request.user
#         enrollments = Enrollment.objects.filter(created_by=request.user)
        
#         # Extract the related courses
#         courses = [enrollment.course for enrollment in enrollments]

#         serializer = CourseListSerializer(courses, many=True)
#         return Response({
#             "courses": serializer.data,
#             "message": "Registered courses retrieved successfully",
#         }, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({
#             "message": str(e),
#         }, status=status.HTTP_400_BAD_REQUEST)


