from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.utils import timezone

@shared_task
def calculate_quiz_score(attempt_id):
    QuizAttempt = apps.get_model('quiz', 'QuizAttempt')
    Question = apps.get_model('quiz', 'Question')
    MultipleChoiceQuestion = apps.get_model('quiz', 'MultipleChoiceQuestion')
    MultipleChoiceQuestionOption = apps.get_model('quiz', 'MultipleChoiceQuestionsOptions')
    TrueFalseQuestion = apps.get_model('quiz', 'TrueFalseQuestion')
    EssayGrade = apps.get_model('quiz', 'EssayGrade')
    EssayQuestionAnswer = apps.get_model('quiz', 'EssayQuestionAnswer')

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
                mc_question = MultipleChoiceQuestion.objects.get(question=question)
                correct_options = MultipleChoiceQuestionOption.objects.filter(mtp_question=mc_question, correct_option=True)
                correct_option_ids = correct_options.values_list('id', flat=True)

                if mc_question.is_many_answers:
                    if set(user_answer) == set(correct_option_ids):
                        user_marks += question.marks
                else:
                    if user_answer in correct_option_ids:
                        user_marks += question.marks

            elif question.question_type == 'boolean':
                true_false_question = TrueFalseQuestion.objects.get(question=question)
                if user_answer == true_false_question.correct_answer:
                    user_marks += question.marks

            elif question.question_type == 'essay':
                essay_answer = EssayQuestionAnswer.objects.filter(
                    created_by=attempt.user,
                    essay_question=question
                ).first()

                # Assuming EssayGrade exists or is calculated elsewhere
                essay_grade = EssayGrade.objects.filter(
                    quiz_attempt=attempt,
                    question=question
                ).first()

                if essay_answer and essay_grade and essay_grade.score:
                    user_marks += essay_grade.score

        except Question.DoesNotExist:
            continue

    # Calculate the percentage score
    percentage_score = (user_marks / total_marks) * 100 if total_marks > 0 else 0

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
