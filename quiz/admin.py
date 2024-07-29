from django.contrib import admin
from .models import (Quiz, Question, MultipleChoiceQuestion,
                      MultipleChoiceQuestionsOptions,
                      TrueFalseQuestion, EssayQuestion,
                        EssayQuestionAnswer, QuizAttempt)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceQuestionsOptions)
admin.site.register(TrueFalseQuestion)
admin.site.register(EssayQuestion)
admin.site.register(EssayQuestionAnswer)
admin.site.register(QuizAttempt)
