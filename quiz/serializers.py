from rest_framework import serializers
from .models import (Quiz, Question, MultipleChoiceQuestion,
                      MultipleChoiceQuestionsOptions
                     , TrueFalseQuestion, EssayQuestion,
                       EssayQuestionAnswer, QuizAttempt, EssayGrade)

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = '__all__'

class MultipleChoiceQuestionsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestionsOptions
        fields = '__all__'

class TrueFalseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrueFalseQuestion
        fields = '__all__'

class EssayQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayQuestion
        fields = '__all__'

class EssayQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayQuestionAnswer
        fields = '__all__'

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = '__all__'

class EssayGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayGrade
        fields = '__all__'

