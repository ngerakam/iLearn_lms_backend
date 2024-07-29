from django.shortcuts import get_object_or_404
from django.utils import timezone
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
                             EssayQuestionAnswerSerializer, QuizAttemptSerializer,
                             EssayGradeSerializer)
from .models import (Quiz, Question, MultipleChoiceQuestion,
                      MultipleChoiceQuestionsOptions,
                      TrueFalseQuestion, EssayQuestion,
                        EssayQuestionAnswer, QuizAttempt, EssayGrade)
from course.models import Course

class QuizListAPIView(APIView):
    def get(self,request,course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            quizzes = course.quizzes.all()
            serializer = QuizSerializer(quizzes, many=True)

            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   

    def post(self,request,course_slug):
        data = request.data
        print(data)
        try:
            course = Course.objects.get(slug=course_slug)
            quiz = Quiz.objects.create(
                course=course,
                title=data.get('title'),
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
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class QuizRetriveAPIView(APIView):
    def get(self,request,course_slug,quiz_slug):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            serializer = QuizSerializer(quiz, many=False)

            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,course_slug,quiz_slug):
        data = request.data
        try:
            course = Course.objects.get(slug=course_slug)
            quiz = Quiz.objects.get(course=course, slug=quiz_slug)
            quiz.title=data.get('title')
            quiz.slug=data.get('slug')
            quiz.description=data.get('description')
            quiz.category=data.get('category')
            quiz.random_order = data.get('random_order')
            quiz.answers_at_end = data.get('answers_at_end')
            quiz.exam_paper = data.get('exam_paper')
            quiz.single_attempt = data.get('single_attempt')
            quiz.pass_mark = data.get('pass_mark')
            quiz.draft = data.get('draft')
            quiz.save()
            serializer = QuizSerializer(quiz, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
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
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
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
            serializer = QuestionSerializer(question, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class QuestionDetailAPIView(APIView):
    def get(self,request,course_slug,quiz_slug,pk=None):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            question = Question.objects.get(pk=pk,quiz=quiz)
            serializer = QuestionSerializer(question, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,course_slug,quiz_slug,pk=None):
        data = request.data
        print(data)
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            question = Question.objects.get(pk=pk, quiz=quiz)
            
            # Update the question fields
            question.question_type = request.data.get('question_type', question.question_type)
            question.text = request.data.get('text', question.text)
            question.marks = request.data.get('marks', question.marks)
            
            question.save()
            
            serializer = QuestionSerializer(question)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,course_slug,quiz_slug,pk=None):
        try:
            quiz = Quiz.objects.get(course__slug=course_slug, slug=quiz_slug)
            question = Question.objects.get(pk=pk,quiz=quiz)
            question.delete()
            return Response({
            "message":f"The question: {question.text} is deleted successfully",
        })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)        

class MultipleChoiceQuestionListAPIView(APIView):
    def get(self,request,course_slug,quiz_slug,pk=None):
        try:
            question = Question.objects.get(pk=pk,quiz__slug=quiz_slug)
            mtp_questions = MultipleChoiceQuestion.objects.filter(question=question)
            serializer = MultipleChoiceQuestionSerializer(mtp_questions, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,course_slug,quiz_slug,pk=None):
        try:
            question = Question.objects.get(pk=pk,quiz__slug=quiz_slug)
            mtp_question = MultipleChoiceQuestion.objects.create(
                question = question,
                is_many_answers = request.data.get("is_many_answers"),
                choice_order = request.data.get("choice_order")
            )
            mtp_question.save()
            serializer = MultipleChoiceQuestionSerializer(mtp_question, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)       


class MultipleChoiceQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MultipleChoiceQuestionSerializer

    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        quiz = get_object_or_404(Quiz, slug=self.kwargs['quiz_slug'], course=course)
        question = get_object_or_404(Question, id=self.kwargs['question_pk'], quiz=quiz)
        return get_object_or_404(MultipleChoiceQuestion, id=self.kwargs['mtp_pk'], question=question)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_many_answers = request.data.get("is_many_answers", instance.is_many_answers)
        instance.choice_order = request.data.get("choice_order", instance.choice_order)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MultipleChoiceQuestionsOptionsListCreateView(APIView):
    def get(self,request,course_slug,quiz_slug,question_pk=None,mtp_pk=None):
        try:
            mtp_question = MultipleChoiceQuestion.objects.get(question__id=question_pk, pk=mtp_pk)
            mtp_options = MultipleChoiceQuestionsOptions.objects.filter(mtp_question=mtp_question)
            serializer = MultipleChoiceQuestionsOptionsSerializer(mtp_options, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, course_slug, quiz_slug, question_pk=None, mtp_pk=None):
        try:
            mtp_question = MultipleChoiceQuestion.objects.get(question__id=question_pk, pk=mtp_pk)
            mtp_option = MultipleChoiceQuestionsOptions.objects.create(
                mtp_question = mtp_question,
                option = request.data.get("option"),
                correct_option = request.data.get("correct_option")
            )
            mtp_option.save()
            serializer = MultipleChoiceQuestionsOptionsSerializer(mtp_option, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MultipleChoiceQuestionsOptionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MultipleChoiceQuestionsOptionsSerializer

    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        quiz = get_object_or_404(Quiz, slug=self.kwargs['quiz_slug'], course=course)
        question = get_object_or_404(Question, id=self.kwargs['question_pk'], quiz=quiz)
        mtp_question = get_object_or_404(MultipleChoiceQuestion,
                                          id=self.kwargs['mtp_pk'], question=question)
        return get_object_or_404(MultipleChoiceQuestionsOptions,
                                  id=self.kwargs['mtpo_pk'], mtp_question=mtp_question)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        instance.option = request.data.get("option", instance.option)
        instance.correct_option = request.data.get("correct_option", instance.correct_option)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TrueFalseQuestionListCreateView(APIView):
    def get(self,request,course_slug,quiz_slug,pk=None):
        try:
            question = Question.objects.get(pk=pk,quiz__slug=quiz_slug)
            questions = TrueFalseQuestion.objects.filter(question=question)
            serializer = TrueFalseQuestionSerializer(questions, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,course_slug,quiz_slug,pk=None):
        try:
            question = Question.objects.get(pk=pk,quiz__slug=quiz_slug)
            tf_question = TrueFalseQuestion.objects.create(
                question = question,
                correct_answer = request.data.get("correct_answer"),
            )
            tf_question.save()
            serializer = TrueFalseQuestionSerializer(tf_question, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class TrueFalseQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrueFalseQuestionSerializer

    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        quiz = get_object_or_404(Quiz, slug=self.kwargs['quiz_slug'], course=course)
        question = get_object_or_404(Question, id=self.kwargs['question_pk'], quiz=quiz)
        return get_object_or_404(TrueFalseQuestion,
                                          id=self.kwargs['tf_pk'], question=question)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.correct_answer = request.data.get("correct_answer", instance.correct_answer)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {
            "message":f"The TrueOrFalse : {instance.id} is deleted successfully",
        },status=status.HTTP_204_NO_CONTENT)

class EssayQuestionListCreateView(generics.ListCreateAPIView):
    def get(self,request,course_slug,quiz_slug,pk=None):
        try:
            question = Question.objects.get(pk=pk,quiz__slug=quiz_slug)
            questions = EssayQuestion.objects.filter(question=question)
            serializer = EssayQuestionSerializer(questions, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,course_slug,quiz_slug,pk=None):
        try:
            question = Question.objects.get(pk=pk,quiz__slug=quiz_slug)
            essy_question = EssayQuestion.objects.create(
                question = question,
                sample_answer = request.data.get("sample_answer"),
            )
            essy_question.save()
            serializer = EssayQuestionSerializer(essy_question, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EssayQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EssayQuestionSerializer

    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        quiz = get_object_or_404(Quiz, slug=self.kwargs['quiz_slug'], course=course)
        question = get_object_or_404(Question, id=self.kwargs['question_pk'], quiz=quiz)
        return get_object_or_404(EssayQuestion,
                                          id=self.kwargs['essay_pk'], question=question)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.sample_answer = request.data.get("sample_answer", instance.sample_answer)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EssayQuestionAnswerListCreateView(generics.ListCreateAPIView):
    def get(self,request,course_slug,quiz_slug,question_pk=None,essay_pk=None):
        try:
            eassy_question = EssayQuestion.objects.get(question__id=question_pk, pk=essay_pk)
            eassy_question_answer = EssayQuestionAnswer.objects.filter(essay_question=eassy_question)
            serializer = EssayQuestionAnswerSerializer(eassy_question_answer, many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, course_slug, quiz_slug, question_pk=None, essay_pk=None):
        try:
            eassy_question = EssayQuestion.objects.get(question__id=question_pk, pk=essay_pk)
            eassy_question_answer = EssayQuestionAnswer.objects.create(
                essay_question = eassy_question,
                is_correct = request.data.get("is_correct"),
                text = request.data.get("text")
            )
            eassy_question_answer.save()
            serializer = EssayQuestionAnswerSerializer(eassy_question_answer, many=False)
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EssayQuestionAnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EssayQuestionAnswerSerializer

    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        quiz = get_object_or_404(Quiz, slug=self.kwargs['quiz_slug'], course=course)
        question = get_object_or_404(Question, id=self.kwargs['question_pk'], quiz=quiz)
        essay_question = get_object_or_404(EssayQuestion,
                                          id=self.kwargs['essay_pk'], question=question)
        return get_object_or_404(EssayQuestionAnswer,
                                  id=self.kwargs['essay_ans_pk'], essay_question=essay_question)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.option = request.data.get("option", instance.option)
        instance.correct_option = request.data.get("correct_option", instance.correct_option)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuizSessionView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.data.get('quiz')
        user_answers = request.data.get('user_answers')
        end_time = timezone.now()

        try:
            quiz_attempt = QuizAttempt.objects.get(user=user, quiz_id=quiz_id, completed=False)
        except QuizAttempt.DoesNotExist:
            return Response({"error": "No active quiz attempt found"}, status=status.HTTP_400_BAD_REQUEST)

        if quiz_attempt.is_time_expired():
            quiz_attempt.end_time = end_time
            quiz_attempt.completed = True
            quiz_attempt.save()
            return Response({"error": "Quiz time limit exceeded"}, status=status.HTTP_400_BAD_REQUEST)

        quiz_attempt.save_answers(user_answers)
        quiz_attempt.complete_attempt()

        return Response({
            "message": "Quiz submitted successfully. Your score will be calculated shortly.",
            "time_taken": (quiz_attempt.end_time - quiz_attempt.start_time).total_seconds() // 60
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.query_params.get('quiz')

        try:
            quiz_attempt = QuizAttempt.objects.get(user=user, quiz_id=quiz_id, completed=False)
        except QuizAttempt.DoesNotExist:
            # Create a new attempt if one doesn't exist
            quiz = Quiz.objects.get(id=quiz_id)
            quiz_attempt = QuizAttempt.objects.create(user=user, quiz=quiz)

        time_remaining = quiz_attempt.time_remaining()

        return Response({
            "attempt_id": quiz_attempt.id,
            "start_time": quiz_attempt.start_time,
            "time_remaining": time_remaining.total_seconds() if time_remaining else None
        })
class ScoreCheckView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        attempt_id = request.query_params.get('attempt_id')

        try:
            quiz_attempt = QuizAttempt.objects.get(id=attempt_id, user=user, completed=True)
        except QuizAttempt.DoesNotExist:
            return Response({"error": "Quiz attempt not found"}, status=status.HTTP_404_NOT_FOUND)

        if quiz_attempt.score_calculated:
            return Response({"score": quiz_attempt.score},status=status.HTTP_200_OK)
        else:
            return Response({"message": "Score is still being calculated"},
                             status=status.HTTP_202_ACCEPTED)
