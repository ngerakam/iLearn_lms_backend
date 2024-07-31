from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.utils import timezone

@shared_task
def calculate_quiz_score(attempt_id):
    QuizAttempt = apps.get_model('quiz', 'QuizAttempt')
    Question = apps.get_model('quiz', 'Question')
    MultipleChoiceQuestionOption = apps.get_model('quiz', 'MultipleChoiceQuestionsOptions')
    TrueFalseQuestion = apps.get_model('quiz', 'TrueFalseQuestion')
    EssayGrade = apps.get_model('quiz', 'EssayGrade')

    attempt = QuizAttempt.objects.get(id=attempt_id)
    quiz = attempt.quiz

    # Initialize total marks and user's marks
    total_marks = 0
    user_marks = 0

    # Calculate total marks and user's marks based on the answers
    for question_id, user_answer in attempt.answers.items():
        try:
            question = Question.objects.get(id=int(question_id))
            total_marks += question.marks

            if question.question_type == 'multi-choice':
                correct_options = MultipleChoiceQuestionOption.objects.filter(question=question, correct_option=True)
                if question.multiple_choice_question.is_many_answers:
                    if set(user_answer) == set([opt.option for opt in correct_options]):
                        user_marks += question.marks
                else:
                    if user_answer == correct_options[0].option:
                        user_marks += question.marks

            elif question.question_type == 'boolean':
                true_false_question = TrueFalseQuestion.objects.get(question=question)
                if user_answer == true_false_question.correct_answer:
                    user_marks += question.marks

            elif question.question_type == 'essay':
                essay_grade = EssayGrade.objects.filter(quiz_attempt=attempt, question=question).first()
                if essay_grade and essay_grade.score:
                    user_marks += essay_grade.score

        except Question.DoesNotExist:
            continue

    # Calculate the percentage score
    if total_marks > 0:
        percentage_score = (user_marks / total_marks) * 100
    else:
        percentage_score = 0

    # Check if the user passed the quiz
    passed = percentage_score >= quiz.pass_mark

    # Update the QuizAttempt with the total score
    attempt.score = user_marks
    attempt.score_calculated = True
    attempt.completed = True
    attempt.end_time = timezone.now()
    attempt.save()

    # Output the result
    result = {
        'total_marks': total_marks,
        'user_marks': user_marks,
        'percentage_score': percentage_score,
        'passed': passed
    }

    return result
