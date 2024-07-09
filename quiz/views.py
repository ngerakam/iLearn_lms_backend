from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .serializers import (QuizSerializer, QuestionSerializer,
                           MultipleChoiceQuestionSerializer,
                             MultipleChoiceQuestionsOptionsSerializer,
                               TrueFalseQuestionSerializer,
                           EssayQuestionSerializer,
                             EssayQuestionAnswerSerializer, UserQuizSessionSerializer)
from .models import (Quiz, Question, MultipleChoiceQuestion,
                      MultipleChoiceQuestionsOptions,
                      TrueFalseQuestion, EssayQuestion,
                        EssayQuestionAnswer, UserQuizSession)
from course.models import Course

class QuizListAPIView(APIView):
    def get(self,request,course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            quizzes = course.quizzes.all()
            serializer = QuizSerializer(quizzes, many=True)

            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   

    def post(self,request,course_slug):
        data = request.data
        try:
            course = Course.objects.get(slug=course_slug)
            quiz = Quiz.objects.create(
                course=course,
                title=data.get('title'),
                slug=data.get('slug'),
                description=data.get('description'),
                category=data.get('category'),
                random_order = data.get('random_order'),
                answers_at_end = data.get('answers_at_end'),
                exam_paper = data.get('exam_paper'),
                single_attempt = data.get('single_attempt'),
                pass_mark = data.get('pass_mark'),
                draft = data.get('draft'),
            )
            quiz.save()
            serializer = QuizSerializer(quiz, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class QuizRetriveAPIView(APIView):
    def get(self,request,course_slug,quiz_slug):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            serializer = QuizSerializer(quiz, many=False)

            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,course_slug,quiz_slug):
        data = request.data
        try:
            course = Course.objects.get(slug=course_slug)
            quiz = Quiz.objects.get(course=course, slug=quiz_slug)
            data.course=course,
            data.title=data.get('title')
            data.slug=data.get('slug')
            data.description=data.get('description')
            data.category=data.get('category')
            data.random_order = data.get('random_order')
            data.answers_at_end = data.get('answers_at_end')
            data.exam_paper = data.get('exam_paper')
            data.single_attempt = data.get('single_attempt')
            data.pass_mark = data.get('pass_mark')
            data.draft = data.get('draft')
            quiz.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,course_slug,quiz_slug):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            quiz.delete()
            return Response({
            "message":f"The quiz: {quiz.title} is deleted successfully",
        })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)        


class QuestionListAPIView(APIView):
    def get(self,request,course_slug,quiz_slug):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            questions = quiz.questions.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,course_slug,quiz_slug,pk=None):
        data = request.data
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            question = Question.objects.create(
                quiz=quiz,
                question_type=data.get('question_type'),
                text = data.get('text'),
                marks = data.get('marks')
            )
            question.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class QuestionDetailAPIView(APIView):
    def get(self,request,course_slug,quiz_slug,pk=None):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            question = Question.objects.get(pk=pk,quiz=quiz)
            serializer = QuestionSerializer(question, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,course_slug,quiz_slug,pk=None):
        data = request.data
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            question = Question.objects.get(pk=pk,quiz=quiz)
            data.quiz=quiz,
            data.question_type=data.get('question_type'),
            data.text = data.get('text'),
            data.marks = data.get('marks')
            question.save()
            serializer = QuestionSerializer(question, many=False)

            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,course_slug,quiz_slug,pk=None):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            question = Question.objects.get(pk=pk,quiz=quiz)
            question.delete()
            return Response({
            "message":f"The question: {question.id} is deleted successfully",
        })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)        

class MultipleChoiceQuestionListAPIView(APIView):
    queryset = MultipleChoiceQuestion.objects.all()
    serializer_class = MultipleChoiceQuestionSerializer

class MultipleChoiceQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MultipleChoiceQuestion.objects.all()
    serializer_class = MultipleChoiceQuestionSerializer

class MultipleChoiceQuestionsOptionsListCreateView(generics.ListCreateAPIView):
    queryset = MultipleChoiceQuestionsOptions.objects.all()
    serializer_class = MultipleChoiceQuestionsOptionsSerializer

class MultipleChoiceQuestionsOptionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MultipleChoiceQuestionsOptions.objects.all()
    serializer_class = MultipleChoiceQuestionsOptionsSerializer

class TrueFalseQuestionListCreateView(generics.ListCreateAPIView):
    queryset = TrueFalseQuestion.objects.all()
    serializer_class = TrueFalseQuestionSerializer

class TrueFalseQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrueFalseQuestion.objects.all()
    serializer_class = TrueFalseQuestionSerializer

class EssayQuestionListCreateView(generics.ListCreateAPIView):
    queryset = EssayQuestion.objects.all()
    serializer_class = EssayQuestionSerializer

class EssayQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EssayQuestion.objects.all()
    serializer_class = EssayQuestionSerializer

class EssayQuestionAnswerListCreateView(generics.ListCreateAPIView):
    queryset = EssayQuestionAnswer.objects.all()
    serializer_class = EssayQuestionAnswerSerializer

class EssayQuestionAnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EssayQuestionAnswer.objects.all()
    serializer_class = EssayQuestionAnswerSerializer

class UserQuizSessionListCreateView(generics.ListCreateAPIView):
    queryset = UserQuizSession.objects.all()
    serializer_class = UserQuizSessionSerializer

class UserQuizSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserQuizSession.objects.all()
    serializer_class = UserQuizSessionSerializer
