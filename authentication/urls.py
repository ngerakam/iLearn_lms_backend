from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (RegisterAPIView, UserProfileAPIView,LoginAPIView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register' ),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(),name='refresh')
]
