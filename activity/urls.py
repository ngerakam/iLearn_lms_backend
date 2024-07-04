from django.urls import path
from .views import (CourseActivityListAPIView, ModuleActivityListAPIView,
                    LessonActivityListAPIView, ActivityLogListAPIView,
                      CreatedCoursesListAPIView, UnpublishedCoursesListAPIView,
                       CompletedCoursesListAPIView, EnrolledCoursesListAPIView,
                        FrontPageCoursesListAPIView )

urlpatterns = [
    path('courses/', CourseActivityListAPIView.as_view()),
    path('modules/', ModuleActivityListAPIView.as_view()),
    path('lessons/', LessonActivityListAPIView.as_view()),
    path('logs/', ActivityLogListAPIView.as_view()),
    #Corses
    path('courses/created/', CreatedCoursesListAPIView.as_view()),
    path('courses/enrolled/', EnrolledCoursesListAPIView.as_view()),
    path('courses/unpublished/', UnpublishedCoursesListAPIView.as_view()),
    path('courses/completed/', CompletedCoursesListAPIView.as_view()),
    path('courses/frontpage/', FrontPageCoursesListAPIView.as_view()),

]
