import json

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
