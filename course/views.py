import time, os ,subprocess
from django.conf import settings
# from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from .models import Course, Lesson, Comment, Category, Quiz
from .serializers import (CourseListSerializer, CourseDetailSerializer,
                          CourseDetailStatusSerializer,
                           LessonListSerializer , CommentSerializer,
                             CategorySerializer, QuizSerializer,
                             UserSerializer)

from authentication.models import User

from docx import Document
from pptx import Presentation

@api_view(['GET'])
def get_quiz(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    quiz = lesson.quizzes.all()
    serializer = QuizSerializer(quiz, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_category(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def create_course(request):
    try:
        course = Course.objects.create(
            title=request.data.get('title'),
            short_description=request.data.get('short_description'),
            long_description=request.data.get('long_description'),
            status=request.data.get('status'),
            created_by=request.user,
        )

        for category_id in request.data.getlist('categories[]'):
            category = Category.objects.get(id=category_id)
            course.categories.add(category)

        image_file = request.data.get('image')
        if image_file:
            course.image.save(image_file.name, image_file)

        course.save()

        serializer = CourseListSerializer(course, many=False)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_course(request, slug):
    try:
        course = Course.objects.get(slug=slug, created_by=request.user)
        
        course.title = request.data.get('title', course.title)
        course.short_description = request.data.get('short_description', course.short_description)
        course.long_description = request.data.get('long_description', course.long_description)
        course.status = request.data.get('status', course.status)
        
        # Update categories
        category_ids = request.data.getlist('categories[]')
        if category_ids:
            categories = Category.objects.filter(id__in=category_ids)
            course.categories.set(categories)
        
        # Update image if provided
        image_file = request.data.get('image')
        if image_file:
            course.image.save(image_file.name, image_file)
        
        course.save()

        serializer = CourseListSerializer(course, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Course.DoesNotExist:
        return Response({'error': 'Course not found or you do not have permission to edit this course.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_courses(request):
    category_id = request.GET.get('category_id','')
    courses = Course.objects.filter(status=Course.PUBLISHED)

    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])

    serializer = CourseListSerializer(courses, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_user_courses(request):
    category_id = request.GET.get('category_id','')
    courses = Course.objects.filter(created_by=request.user)

    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])

    serializer = CourseListSerializer(courses, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_frontpage_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED)[0:4]
    serializer = CourseListSerializer(courses, many=True)

    return Response(serializer.data)

@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
def get_course(request, slug):
    course = Course.objects.get(slug=slug)
    course_serializer = CourseDetailSerializer(course)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)

    if request.user.is_authenticated:
        course_data = course_serializer.data
        lesson_data = lesson_serializer.data
    else:
        course_data = {}
        lesson_data = lesson_serializer.data

    data = {
        'course' : course_data,
        'lessons' : lesson_data
    }

    return Response(data)

@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
def get_course_with_status(request, slug):
    course = Course.objects.get(slug=slug)
    course_serializer = CourseDetailStatusSerializer(course)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)

    if request.user.is_authenticated:
        course_data = course_serializer.data
        lesson_data = lesson_serializer.data

    else:
        course_data = {}
        lesson_data = lesson_serializer.data


    data = {
        'course' : course_data,
        'lessons' : lesson_data
    }

    return Response(data)

@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
def get_course_lessons(request, slug):
    course = Course.objects.get(slug=slug)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)

    if request.user.is_authenticated:
        lesson_data = lesson_serializer.data
    else:
        lesson_data = lesson_serializer.data

    data = {
        'lessons' : lesson_data,
    }

    return Response(data)

@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
def get_created_course(request, slug):
    course = Course.objects.get(slug=slug)
    course_serializer = CourseDetailSerializer(course)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)

    if request.user.is_authenticated:
        course_data = course_serializer.data
        lesson_data = lesson_serializer.data
    else:
        course_data = {}
        lesson_data = lesson_serializer.data
        
    data = {
        'course' : course_data,
        'lessons' : lesson_data
    }

    return Response(data)

@api_view(['GET'])
def get_comment(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    serializer = CommentSerializer(lesson.comments.all(), many=True)

    return Response(serializer.data)

@api_view(['POST'])
def add_comment(request, course_slug, lesson_slug):
    data = request.data
    name = data.get('name')
    content = data.get('content')
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    comment = Comment.objects.create(course=course, lesson=lesson, name=name,
                                      content=content, created_by=request.user)
    
    serializer = CommentSerializer(comment)
    
    return Response(serializer.data)

@api_view(['GET'])
def get_author_courses(request, user_id):
    user = User.objects.get(pk=user_id)
    courses = user.courses.filter(status=Course.PUBLISHED)

    user_serializer = UserSerializer(user, many=False)
    courses_serializer = CourseListSerializer(courses, many=True)

    return Response({
            'courses': courses_serializer.data,
            'created_by': user_serializer.data
         })

@api_view(['GET'])
def get_user_lesson(request,course_slug,lesson_slug):
    user = request.user
    lesson = Lesson.objects.get(slug=lesson_slug,
                                 course__slug=course_slug,
                                   course__created_by=user)

    serializer = LessonListSerializer(lesson, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def add_lessons_to_course(request, course_slug):
    user = request.user
    
    try:
        course = Course.objects.get(slug=course_slug, created_by=user)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found or you do not have permission to add lessons to this course.'}, status=status.HTTP_404_NOT_FOUND)

    lesson_type = request.data.get('lesson_type')

    def extract_quiz_data(data):
        quiz_data = {}
        for key, value in data.items():
            if key.startswith('quizObject'):
                parts = key.split('[')
                index = int(parts[1][:-1])
                field = parts[2][:-1]
                if index not in quiz_data:
                    quiz_data[index] = {}
                quiz_data[index][field] = value[0]
        return quiz_data

    if lesson_type in ['article', 'video', 'file', 'quiz']:
        lesson_data = {
            'course': course,
            'title': request.data.get('title'),
            'short_description': request.data.get('short_description'),
            'status': request.data.get('status'),
        }

        if lesson_type == 'article':
            lesson_data['lesson_type'] = 'article'
            lesson_data['long_description'] = request.data.get('long_description')
        elif lesson_type == 'video':
            lesson_data['lesson_type'] = 'video'
            video_file = request.data.get('video')
            if video_file:
                lesson_data['video'] = video_file
            else:
                lesson_data['youtube_id'] = request.data.get('youtube_id')
        elif lesson_type == 'file':
            lesson_data['lesson_type'] = 'file'
            document_file = request.data.get('document')
            if document_file:
                lesson_data['file'] = document_file
        elif lesson_type == 'quiz':
            lesson_data['lesson_type'] = 'quiz'
            
            quiz_data = extract_quiz_data(request.data)

            lesson = Lesson.objects.create(**lesson_data)

            for index, data in quiz_data.items():
                question = data.get('question', None)
                op1 = data.get('op1', None)
                op2 = data.get('op2', None)
                op3 = data.get('op3', None)
                answer = data.get('answer', None)

                # Create the Quiz object without using defaults
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    question=question,
                    op1=op1,
                    op2=op2,
                    op3=op3,
                    answer=answer
                )

            serializer = LessonListSerializer(lesson, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid lesson type.'}, status=status.HTTP_400_BAD_REQUEST)

        lesson = Lesson.objects.create(**lesson_data)
        serializer = LessonListSerializer(lesson, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid lesson type.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_lessons_to_course(request, course_slug, lesson_slug):
    user = request.user
    
    try:
        course = Course.objects.get(slug=course_slug, created_by=user)
        lesson = Lesson.objects.get(slug=lesson_slug, course=course)
    except (Course.DoesNotExist, Lesson.DoesNotExist):
        return Response({'error': 'Lesson not found or you do not have permission to edit this lesson.'}, status=status.HTTP_404_NOT_FOUND)

    lesson_type = request.data.get('lesson_type')

    def extract_quiz_data(data):
        quiz_data = {}
        for key, value in data.items():
            if key.startswith('quizObject'):
                parts = key.split('[')
                index = int(parts[1][:-1])
                field = parts[2][:-1]
                if index not in quiz_data:
                    quiz_data[index] = {}
                quiz_data[index][field] = value[0]
        return quiz_data

    if lesson_type in ['article', 'video', 'file', 'quiz']:
        lesson.title = request.data.get('title', lesson.title)
        lesson.short_description = request.data.get('short_description', lesson.short_description)
        lesson.status = request.data.get('status', lesson.status)
        lesson.lesson_type = lesson_type

        if lesson_type == 'article':
            lesson.long_description = request.data.get('long_description', lesson.long_description)
        elif lesson_type == 'video':
            video_file = request.data.get('video')
            if video_file:
                lesson.video = video_file
                lesson.youtube_id = None  # Clear youtube_id if video file is provided
            else:
                lesson.youtube_id = request.data.get('youtube_id', lesson.youtube_id)
        elif lesson_type == 'file':
            document_file = request.data.get('document')
            if document_file:
                lesson.file = document_file
        elif lesson_type == 'quiz':
            quiz_data = extract_quiz_data(request.data)

            # Clear existing quizzes for the lesson
            Quiz.objects.filter(lesson=lesson).delete()

            for index, data in quiz_data.items():
                question = data.get('question')
                op1 = data.get('op1')
                op2 = data.get('op2')
                op3 = data.get('op3')
                answer = data.get('answer')

                Quiz.objects.create(
                    lesson=lesson,
                    question=question,
                    op1=op1,
                    op2=op2,
                    op3=op3,
                    answer=answer
                )

        lesson.save()

        serializer = LessonListSerializer(lesson, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid lesson type.'}, status=status.HTTP_400_BAD_REQUEST)