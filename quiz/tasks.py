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
                mc_question = question.multiple_choice_question
                correct_options = mc_question.options.filter(correct_option=True)
                user_selected_options = answer

                if mc_question.is_many_answers:
                    # Calculate the marks for each correct option
                    correct_option_marks = question.marks / correct_options.count()
                    print("correct_options",correct_options)
                    print("user_selected_options",user_selected_options)
                    print("correct_option_marks",correct_option_marks)
                    # Calculate the total score for the question
                    question_score = 0
                    for option in user_selected_options:
                        for correct_option in correct_options:
                            if option == correct_option.option:  # comparing with the 'option' field
                                question_score += correct_option_marks
                                print("MCQ option",option)
                                print("MCQ many score",question_score)
                else:
                    correct_option = correct_options.first()
                    if answer == correct_option.option:  # comparing with the 'option' field
                        print(answer)
                        print(correct_option)
                        question_score = question.marks
                    else:
                        question_score = 0

            elif question.question_type == 'boolean':
                true_false_question = question.true_false_question
                question_score = question.marks if answer == true_false_question.correct_answer else 0

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

            else:
                logger.warning(f"Unknown question type {question.question_type} for question {question_id}")
                question_score = 0

            user_marks += question_score
            logger.debug(f"Score for question {question_id}: {question_score}")

        except Exception as e:
            logger.error(f"Error processing question {question_id}: {str(e)}")
            # Continue with next question instead of stopping the entire calculation

    logger.info(f"All questions processed. Total marks: {total_marks}, User marks: {user_marks}")

    # Calculate the percentage score
    percentage_score = (user_marks / total_marks) * 100 if total_marks > 0 else 0

    # Check if the user passed the quiz
    passed = percentage_score >= quiz.pass_mark

    # Update the QuizAttempt with the total score
    attempt.score = user_marks
    attempt.score_calculated = True
    attempt.save()

    logger.info(f"Quiz attempt updated. Final score: {user_marks}, Passed: {passed}")

    # Return the result
    return {
        'total_marks': int(total_marks),
        'user_marks': int(user_marks),
        'percentage_score': percentage_score,
        'passed': passed,
        'all_essays_graded': attempt.all_essays_graded()
    }

def all_essays_graded(attempt):
    essay_questions = attempt.quiz.questions.filter(question_type='essay')
    graded_essays = attempt.essay_grades.all()
    return essay_questions.count() == graded_essays.count()