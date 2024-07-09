from django.urls import path
from .views import *

urlpatterns = [
    path('courses/<str:course_slug>/',QuizListAPIView.as_view()),
    path('courses/<str:course_slug>/quiz/<str:quiz_slug>/',QuizRetriveAPIView.as_view()),
    
]