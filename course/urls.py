from django.urls import path
from course import views

urlpatterns = [
    path('', views.get_courses),
    path('my-courses/', views.get_user_courses),
    path('get_frontpage_courses/', views.get_frontpage_courses),
    path('get_categories/', views.get_category),
    path('get_author_courses/<int:user_id>/', views.get_author_courses),
    path('create-course/', views.create_course),
    path('create-course/<slug:course_slug>/create-lesson/', views.add_lessons_to_course),
    path('update-course/<slug:course_slug>/update-lesson/', views.update_lessons_to_course),
    path('<slug:slug>/create-lesson/', views.get_created_course),
    path('<slug:slug>/', views.get_course),
    path('<slug:slug>/fetch-course-lesson/', views.get_course_lessons),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.add_comment),
    path('<slug:course_slug>/<slug:lesson_slug>/get-comments/', views.get_comment),
    path('<slug:course_slug>/<slug:lesson_slug>/get-quiz/', views.get_quiz),
]
