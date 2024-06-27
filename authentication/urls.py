from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (RegisterAPIView, UserProfileAPIView,SiteSetupDetailAPIView
                    , UserListView, UserRetriveView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register' ),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(),name='refresh'),
    path('site-setup/', SiteSetupDetailAPIView.as_view(), name='site-setup-detail'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('profile/<str:pk>/', UserProfileAPIView.as_view(), name='profile-update'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<str:pk>/', UserRetriveView.as_view(), name='user-details'),
    path('user/<str:pk>/delete/', UserRetriveView.as_view(), name='user-delete'),
]
