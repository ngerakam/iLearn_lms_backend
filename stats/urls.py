from django.urls import path
from .views import (EnrollmentCountView, CompletionStatusView,
                    TotalUserCourses, CourseActivityAPIView,
                    ModuleActivityAPIView, LessonActivityAPIView)

urlpatterns = [
    path('enrollment-count/', EnrollmentCountView.as_view(), name='enrollment-count'),
    path('completion-status/', CompletionStatusView.as_view(), name='completion-status'),
    path('my-total-courses/', TotalUserCourses.as_view(), name='my-total-courses'),
    # path('completed-course-activities/<str:pk>/', CourseCompleteionActivitiesView.as_view(), name='completed-course-activities'),
]
