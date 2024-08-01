from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.core.validators import MaxValueValidator, validate_comma_separated_integer_list
from autoslug import AutoSlugField
from django.utils import timezone
from datetime import timedelta
from .tasks import calculate_quiz_score


CONTENT= 'content'
RANDOM = 'random'
NONE = 'none'

CHOICE_ORDER_OPTIONS = (
    (CONTENT, "Content"),
    (RANDOM, "Random"),
    (NONE, "None"),
)

ASSIGNMENT = 'assignment'
EXAM = 'exam'
PRACTICE = 'practice'

CATEGORY_OPTIONS = (
    (ASSIGNMENT, "Assignment"),
    (EXAM, "Exam"),
    (PRACTICE, "Practice Quiz"),
)

class Quiz(models.Model):
    course = models.ForeignKey('course.Course', related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    description = models.TextField(blank=True)
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=20, blank=True)
    random_order = models.BooleanField(default=False)
    answers_at_end = models.BooleanField(default=False)
    exam_paper = models.BooleanField(default=False)
    single_attempt = models.BooleanField(default=False)
    pass_mark = models.SmallIntegerField(default=50, validators=[MaxValueValidator(100)])
    draft = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes", null=True, blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    ESSAY = 'essay'
    BOOLEAN = 'boolean'
    MULTIPLE_CHOICE = 'multi-choice'
    
    QUESTION_TYPES = (
        (ESSAY, 'Essay'),
        (BOOLEAN, 'Boolean'),
        (MULTIPLE_CHOICE, 'Multiple Choice')
    )
    
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    text = models.TextField()
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.text

class MultipleChoiceQuestion(models.Model):
    question = models.OneToOneField(Question, related_name='multiple_choice_question', on_delete=models.CASCADE)
    is_many_answers = models.BooleanField(default=False)
    choice_order = models.CharField(max_length=30, choices=CHOICE_ORDER_OPTIONS, blank=True, null=True)

    def get_choices(self):
        return self.order_choices(MultipleChoiceQuestionsOptions.objects.filter(mtp_question=self))

    def order_choices(self, queryset):
        if self.choice_order == "content":
            return queryset.order_by("option")
        if self.choice_order == "random":
            return queryset.order_by("?")
        return queryset

    def __str__(self):
        return f"Multiple Question {self.question.text}  has multiple answers {self.is_many_answers} with Choice order {self.choice_order}"

class MultipleChoiceQuestionsOptions(models.Model):
    mtp_question = models.ForeignKey(MultipleChoiceQuestion, related_name='options', on_delete=models.CASCADE)
    option = models.CharField(max_length=255, blank=True, null=True)
    correct_option = models.BooleanField(default=False)

    def __str__(self):
        return f"Multiple Question {self.mtp_question.question.text} for Multiple answer {self.option} correct? {self.correct_option}"

class TrueFalseQuestion(models.Model):
    question = models.OneToOneField(Question, related_name='true_false_question', on_delete=models.CASCADE)
    correct_answer = models.BooleanField()

    def __str__(self):
        return f"Question {self.question.text} for answer: {self.correct_answer}"

class EssayQuestion(models.Model):
    question = models.OneToOneField(Question, related_name='essay_question', on_delete=models.CASCADE)
    sample_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Question {self.question.text} for quiz {self.sample_answer}"

class EssayQuestionAnswer(models.Model):
    essay_question = models.ForeignKey(EssayQuestion, related_name='essay_answers',
                                        on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    text = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='essay_answers', on_delete=models.CASCADE)
    class Meta:
        unique_together=('created_by','essay_question')
    def __str__(self):
        return f"Question {self.essay_question.question.text} for answer {self.text}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz_attempts', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', related_name='attempts', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    answers = models.JSONField(default=dict)
    score_calculated = models.BooleanField(default=False)

    class Meta:
        unique_together=('user','quiz')

    def save_answers(self, answers_dict):
        """
        Save user answers to the answers field.
        """
        for question_id, answer_data in answers_dict.items():
            self.answers[str(question_id)] = answer_data['answer']
            question = self.quiz.questions.get(id=int(question_id))
            if question.question_type == 'essay':
                EssayGrade.objects.create(
                    quiz_attempt=self,
                    question=question,
                    student=self.user,
                    grader=None,
                    score=None,
                    feedback=''
                )
        self.save()

    def complete_attempt(self):
        """
        Mark the attempt as completed, set the end time, and trigger the score calculation task.
        """
        if not self.completed:
            self.completed = True
            self.end_time = timezone.now()
            self.save()
            calculate_quiz_score.delay(self.id)  # Use the task here

    def all_essays_graded(self):
        essay_questions = self.quiz.questions.filter(question_type='essay')
        graded_essays = self.essay_grades.all()
        return essay_questions.count() == graded_essays.count()

    def __str__(self):
        return f"User: {self.user.email}'s attempt on {self.quiz.title}"

class EssayGrade(models.Model):
    quiz_attempt = models.ForeignKey('QuizAttempt', on_delete=models.CASCADE, related_name='essay_grades')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    grader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='essay_grader')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='essay_student')
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    graded_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('quiz_attempt', 'question')

    def __str__(self):
        return f"Essay grade for {self.quiz_attempt.quiz.title} - Question {self.question.text}"
from django.db import transaction

@receiver(post_save, sender=EssayGrade)
def recalculate_quiz_score_on_essay_grade_update(sender, instance, **kwargs):
    if not kwargs.get('created') and instance.score is not None:
        with transaction.atomic():
            instance.quiz_attempt.score_calculated = False
            instance.quiz_attempt.save(update_fields=['score_calculated'])
            calculate_quiz_score.delay(instance.quiz_attempt.id)