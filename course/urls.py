from django.urls import path
from .views import (LearningPathListAPIView, LearningPathAPIView, 
                    CategoryListAPIView, CategoryAPIView, CoursesListAPIView,
                    CoursesAPIView, ModuleListAPiView, ModuleAPiView,
                    LessonListAPIView, LessonAPIView, CommentListAPIView,
                    CommentAPIView, EnrollmentListAPIView, ProgressListAPIView)

urlpatterns = [
    path('learning-paths/', LearningPathListAPIView.as_view()),
    path('learning-paths/<str:lp_slug>/', LearningPathAPIView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<str:cat_slug>/', CategoryAPIView.as_view()),
    path('', CoursesListAPIView.as_view()),
    path('<str:course_slug>/', CoursesAPIView.as_view()),
    path('<str:course_slug>/modules/', ModuleListAPiView.as_view()),
    path('<str:course_slug>/modules/<str:mod_slug>/', ModuleAPiView.as_view()),
    path('<str:course_slug>/modules/<str:mod_slug>/lessons/', LessonListAPIView.as_view()),
    path('<str:course_slug>/modules/<str:mod_slug>/lessons/<str:lesson_slug>/', LessonAPIView.as_view()),
    path('<str:course_slug>/modules/<str:mod_slug>/lessons/<str:lesson_slug>/comments/', CommentListAPIView.as_view()),
    path('<str:course_slug>/modules/<str:mod_slug>/lessons/<str:lesson_slug>/comments/<str:pk>/', CommentAPIView.as_view()),
    #Enrollment and Progress urls
    path('<str:course_slug>/enrollments/', EnrollmentListAPIView.as_view()),
    path('<str:course_slug>/progress/', ProgressListAPIView.as_view()),
]
