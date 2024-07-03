from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.core.validators import MaxValueValidator, validate_comma_separated_integer_list
from autoslug import AutoSlugField

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
    correct_option = models.BooleanField()

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
    essay_question = models.ForeignKey(EssayQuestion, related_name='essay_answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    text = models.TextField()

    def __str__(self):
        return f"Question {self.essay_question.question.text} for answer {self.text}"

class UserQuizSession(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sessions')
    quiz = models.ForeignKey(Quiz, related_name='sessions', on_delete=models.CASCADE)
    question_order = models.CharField(max_length=30, choices=CHOICE_ORDER_OPTIONS, blank=True, null=True)
    question_list = models.CharField(max_length=1024, validators=[validate_comma_separated_integer_list])
    incorrect_questions = models.CharField(max_length=1024, blank=True, validators=[validate_comma_separated_integer_list])
    current_score = models.IntegerField()
    complete = models.BooleanField(default=False)
    user_answers = models.TextField(blank=True, default="{}")
    take_time = models.DurationField(null=True, blank=True)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    grade = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'UserQuizSessions'

    def __str__(self):
        return f"{self.user} - {self.quiz}"

    def save(self, *args, **kwargs):
        if self.end and self.start:
            self.take_time = self.end - self.start  
        super().save(*args, **kwargs)

@receiver(post_save, sender=UserQuizSession)
def set_question_order(sender, instance, created, **kwargs):
    if created:
        quiz = instance.quiz
        questions = quiz.questions.all()

        # Determine the order of questions based on quiz settings
        if instance.question_order == CONTENT:
            # No additional ordering needed if questions are already in content order
            pass
        elif instance.question_order == RANDOM:
            questions = instance.quiz.questions.order_by("?")
        elif instance.question_order == NONE:
            # No specific order, use default queryset order
            pass

        # Generate question order and update the instance
        instance.question_order = ",".join([str(q.id) for q in questions])
        instance.question_list = instance.question_order
        instance.save()

        # Ensure correct ordering of choices if applicable
        for question in questions:
            if question.question_type == Question.MULTIPLE_CHOICE:
                multiple_choice_question = question.multiple_choice_question
                options = multiple_choice_question.order_choices(multiple_choice_question.options.all())
                multiple_choice_question.options.set(options)
