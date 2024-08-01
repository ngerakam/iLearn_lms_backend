from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.utils import timezone

def extract_quiz_info(data):
    quiz_id = data.get('quiz')
    user_answers = data.get('user_answers', {})
    question_answers = []
    
    for question_id, answer_data in user_answers.items():
        question_info = {
            'questionId': int(question_id),
            'answer': answer_data.get('answer', None),
            'question_type': answer_data.get('question_type', 'unknown')
        }
        question_answers.append(question_info)
    
    return {
        'quiz_id': quiz_id,
        'user_answers': user_answers,
        'question_answers': question_answers
    }

def extract_question_data(data):
    return [
        {
            "question__pk": item["questionId"],
            "answer": item["answer"],
            "question_type": item["question_type"]
        }
        for item in data
    ]

@shared_task
def calculate_quiz_score(attempt_id):
    QuizAttempt = apps.get_model('quiz', 'QuizAttempt')
    print(f"Quiz attempt: {attempt}")
    print(f"Answers: {attempt.answers}")
    if not attempt.answers:
        print(f"Error: No answers found for quiz attempt {attempt_id}")
        return None
    Question = apps.get_model('quiz', 'Question')
    MultipleChoiceQuestion = apps.get_model('quiz', 'MultipleChoiceQuestion')
    MultipleChoiceQuestionOption = apps.get_model('quiz', 'MultipleChoiceQuestionsOptions')
    TrueFalseQuestion = apps.get_model('quiz', 'TrueFalseQuestion')
    EssayGrade = apps.get_model('quiz', 'EssayGrade')
    EssayQuestion = apps.get_model('quiz', 'EssayQuestion')
    EssayQuestionAnswer = apps.get_model('quiz', 'EssayQuestionAnswer')


    attempt = QuizAttempt.objects.get(id=attempt_id)
    quiz = attempt.quiz
    # Initialize total marks and user's marks
    total_marks = 0
    user_marks = 0

    # Extract question data
    obj = extract_quiz_info(attempt.answers)
    question_answers = obj['question_answers']
    user_answers = extract_question_data(question_answers)

    # Calculate total marks and user's marks based on the answers
    for item in user_answers:
        try:
            question = Question.objects.get(id=item["question__pk"], question_type=item["question_type"])
            total_marks += question.marks

            if question.question_type == 'multi-choice':
                mc_question = MultipleChoiceQuestion.objects.get(question=question)
                correct_options = MultipleChoiceQuestionOption.objects.filter(mtp_question=mc_question, correct_option=True)
                correct_option_ids = set(correct_options.values_list('id', flat=True))

                if mc_question.is_many_answers:
                    marks_per_option = question.marks / correct_options.count()
                    user_selected_correct_options = set(item["answer"]) & correct_option_ids
                    user_marks += len(user_selected_correct_options) * marks_per_option
                else:
                    if item["answer"] in correct_option_ids:
                        user_marks += question.marks

            elif question.question_type == 'boolean':
                true_false_question = TrueFalseQuestion.objects.get(question=question)
                if item["answer"] == true_false_question.correct_answer:
                    user_marks += question.marks

            elif question.question_type == 'essay':
                essay_grade = EssayGrade.objects.filter(
                    quiz_attempt=attempt,
                    question=question
                ).first()

                if essay_grade and essay_grade.score is not None:
                    user_marks += essay_grade.score
                else:
                    # If the essay hasn't been graded yet, we can't calculate the final score
                    return None  # or you could raise an exception here

        except Question.DoesNotExist:
            continue

    # Check if all essays are graded
    if not attempt.all_essays_graded():
        return None  # or raise an exception

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