from django.urls import path
from .views import *

urlpatterns = [
    #Quiz views
    path('courses/<str:course_slug>/',QuizListAPIView.as_view()),
    path('courses/<str:course_slug>/quiz/<str:quiz_slug>/',QuizRetriveAPIView.as_view()),
    #Question views
    path('courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/'
         ,QuestionListAPIView.as_view()),
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:pk>/'
        ,QuestionDetailAPIView.as_view()),
        #Multiple choice questions & options views
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:pk>/mtp_types/',
        MultipleChoiceQuestionListAPIView.as_view()),
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:question_pk>/mtp_types/<str:mtp_pk>/',
        MultipleChoiceQuestionDetailView.as_view()),
                #options
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:question_pk>/mtp_types/<str:mtp_pk>/options/',
        MultipleChoiceQuestionsOptionsListCreateView.as_view()
    ),
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:question_pk>/mtp_types/<str:mtp_pk>/options/<str:mtpo_pk>/',
        MultipleChoiceQuestionsOptionsDetailView.as_view()
    ),
    #true or false questions views
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:pk>/tf_types/'
        ,TrueFalseQuestionListCreateView.as_view()),
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:question_pk>/tf_types/<str:tf_pk>/',
        TrueFalseQuestionDetailView.as_view()),
    #Eassy Question
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:pk>/essay_types/'
        ,EssayQuestionListCreateView.as_view()),
    path(
        'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:question_pk>/essay_types/<str:essay_pk>/',
        EssayQuestionDetailView.as_view()),
    #Eassy Question Answers essay_pk
    path(
'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:question_pk>/essay_types/<str:essay_pk>/answers/',
        EssayQuestionAnswerListCreateView.as_view()),
    path(
'courses/<str:course_slug>/quiz/<str:quiz_slug>/questions/<str:question_pk>/essay_types/<str:essay_pk>/answers/<str:essay_ans_pk/',
        EssayQuestionAnswerListCreateView.as_view()),
    #User Sessions --- Test
    path('courses/<str:course_slug>/quiz/<str:quiz_slug>/sessions/',UserQuizSessionListCreateView.as_view()),
    path('courses/<str:course_slug>/quiz/<str:quiz_slug>/sessions/<str:session_pk>/',UserQuizSessionListCreateView.as_view()),
]