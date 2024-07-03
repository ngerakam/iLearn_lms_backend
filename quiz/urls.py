from django.urls import path
from .views import *

urlpatterns = [
    path('/<str:slug>/',QuizListAPIView.as_view()),
    path('/<str:slug>/<str:slug>/',QuizRetriveAPIView.as_view()),
    
]