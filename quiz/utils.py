from django.db.models import Sum
from django.utils import timezone
import json
from .models import *

def extract_question_data(data):
    """
    Extract question__pk and answer from the given data structure.
    
    Args:
    data (list): A list of dictionaries containing question data.
    
    Returns:
    list: A list of dictionaries with 'question__pk' and 'answer' keys.
    """
    extracted_data = [
        {
            "question__pk": item["questionId"],
            "answer": item["answer"]["answer"],
            "question_type": item["answer"]["question_type"]
        }
        for item in data
    ]
    return extracted_data

def extract_quiz_info(data):
    quiz_id = data.get('quiz')
    user_answers = data.get('user_answers', {})
    question_answers = []
    
    for question_id, answer_data in user_answers.items():
        question_info = {
            'questionId': int(question_id),
            'answer': answer_data.get('answer', None),  # Default to None if not present
            'question_type': answer_data.get('question_type', 'unknown')  # Default to 'unknown'
        }
        question_answers.append(question_info)
    
    return {
        'quiz_id': quiz_id,
        'user_answers': user_answers,
        'question_answers': question_answers
    }


def check_answers(quiz_info):
    from quiz.models import Question  # Import inside the function to avoid circular import
    question_answers = quiz_info['question_answers']
    correct_count = 0
    
    for q in question_answers:
        question_id = q['questionId']
        user_answer = q['answer']
        question_type = q['question_type']
        
        try:
            question = Question.objects.get(id=question_id)
            
            if question_type == 'multi-choice':
                correct_options = question.multiple_choice_question.options.filter(correct_option=True)
                if question.multiple_choice_question.is_many_answers:
                    if set(user_answer) == set([opt.option for opt in correct_options]):
                        correct_count += 1
                else:
                    if user_answer[0] in [opt.option for opt in correct_options]:
                        correct_count += 1
            
            elif question_type == 'boolean':
                if user_answer == question.true_false_question.correct_answer:
                    correct_count += 1
            
            elif question_type == 'essay':
                essay_grade = question.essay_question.essay_answers.filter(created_by=quiz_info['user']).first()
                if essay_grade and essay_grade.is_correct:
                    correct_count += 1

        except Question.DoesNotExist:
            print(f"Question with id {question_id} does not exist.")
    
    return correct_count


import logging
from celery import shared_task


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
                correct_option_ids = set(correct_options.values_list('id', flat=True))
                user_selected_options = set(answer)

                if mc_question.is_many_answers:
                    # Calculate the score for each correct option
                    correct_option_scores = []
                    for option_id in user_selected_options & correct_option_ids:
                        option = MultipleChoiceQuestionOption.objects.get(id=option_id)
                        correct_option_scores.append(option.marks)

                    # Calculate the score for each incorrect option
                    incorrect_option_scores = []
                    for option_id in user_selected_options - correct_option_ids:
                        option = MultipleChoiceQuestionOption.objects.get(id=option_id)
                        incorrect_option_scores.append(option.marks)

                    # Calculate the total score for the question
                    question_score = sum(correct_option_scores) - sum(incorrect_option_scores)
                    question_score /= correct_options.count()
                else:
                    correct_option_id = correct_options.first().id
                    if answer == str(correct_option_id):
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