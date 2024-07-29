from celery import shared_task
from django.apps import apps

@shared_task
def calculate_quiz_score(attempt_id):
    QuizAttempt = apps.get_model('quiz', 'QuizAttempt')
    attempt = QuizAttempt.objects.get(id=attempt_id)
    
    total_score = 0
    for question_id, answer in attempt.answers.items():
        question = attempt.quiz.questions.get(id=question_id)
        if question.question_type == 'multi-choice':
            correct_option = question.multiple_choice_question.options.get(correct_option=True)
            if answer == correct_option.option:
                total_score += question.marks
        elif question.question_type == 'boolean':
            if answer == question.true_false_question.correct_answer:
                total_score += question.marks
        elif question.question_type == 'essay':
            essay_grade = attempt.essay_grades.filter(question=question).first()
            if essay_grade and essay_grade.score is not None:
                total_score += essay_grade.score

    attempt.score = total_score
    attempt.save()

    return total_score
