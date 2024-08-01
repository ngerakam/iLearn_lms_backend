import logging
from celery import shared_task
from django.db.models import F
from django.db import transaction
from .models import *

logger = logging.getLogger(__name__)

@shared_task
def run_calculate_quiz_score(attempt_id):
    """
    Calculate the score for a given quiz attempt using Django models.
    
    :param attempt_id: ID of the QuizAttempt
    :return: Dict with score results or error message
    """
    logger.info(f"Starting score calculation for attempt ID: {attempt_id}")
    
    try:
        attempt = QuizAttempt.objects.get(id=attempt_id)
    except QuizAttempt.DoesNotExist:
        logger.error(f"Quiz attempt with ID {attempt_id} not found")
        return {"error": "Quiz attempt not found"}

    quiz = attempt.quiz
    user_answers = attempt.answers

    logger.info(f"Processing answers for quiz: {quiz.title}")

    # Initialize total marks and user's marks
    total_marks = 0
    user_marks = 0

    # Calculate total marks and user's marks based on the answers
    for question_id, answer in user_answers.items():
        try:
            question = Question.objects.get(id=int(question_id), quiz=quiz)
        except Question.DoesNotExist:
            logger.warning(f"Question with ID {question_id} not found, skipping")
            continue

        total_marks += question.marks
        logger.debug(f"Processing question {question_id} of type {question.question_type}")

        try:
            if question.question_type == 'multi-choice':
                multiple_choice_question = question.multiple_choice_question
                correct_options = multiple_choice_question.options.filter(correct_option=True)
                correct_option_ids = [option.id for option in correct_options]
                user_answer_ids = answer['answer']
                if set(user_answer_ids) == set(correct_option_ids):
                    user_marks += question.marks
            elif question.question_type == 'true-false':
                true_false_question = question.true_false_question
                if answer['answer'] == true_false_question.correct_answer:
                    user_marks += question.marks
            elif question.question_type == 'essay':
                essay_grade = EssayGrade.objects.filter(
                    quiz_attempt=attempt,
                    question=question
                ).first()

                if essay_grade and essay_grade.score is not None:
                    question_score = essay_grade.score
                else:
                    logger.warning(f"Essay for question {question_id} not graded yet")
                    question_score = 0  # We'll continue calculation, but mark this as potentially incomplete
        except Exception as e:
            logger.error(f"Error processing question {question_id}: {str(e)}")
            # Continue with next question instead of stopping the entire calculation

    logger.info(f"All questions processed. Total marks: {total_marks}, User marks: {user_marks}")

    # Calculate the percentage score
    percentage_score = (user_marks / total_marks) * 100 if total_marks > 0 else 0

    # Check if the user passed the quiz
    passed = percentage_score >= quiz.pass_mark

    with transaction.atomic():
        attempt.score = user_marks
        attempt.completed = True
        attempt.save()

        if all_essays_graded(attempt):
            attempt.score_calculated = True
            attempt.save()

    logger.info(f"Quiz attempt updated. Final score: {user_marks}, Passed: {passed}")

    # Return the result
    return {
        'total_marks': total_marks,
        'user_marks': user_marks,
        'percentage_score': percentage_score,
        'passed': passed,
        'all_essays_graded': all_essays_graded(attempt)
    }

def all_essays_graded(attempt):
    essay_questions = attempt.quiz.questions.filter(question_type='essay')
    graded_essays = attempt.essay_grades.all()
    return essay_questions.count() == graded_essays.count()