# will take too much time to complete
# Total 1272 questions in one jsonl file

from question_maker import question_list
from RAG_and_LLM import MCQSolver
def validate_model(questions_list):
    correct_predictions = 0
    total_questions = len(questions_list)
    print(f"Total Questions: {total_questions}")
    for question_data in questions_list:
        question = question_data['question']
        options = question_data['options']
        correct_answer = question_data['answer_idx']
        predicted_answer = MCQSolver(question, options)  
        if predicted_answer == correct_answer:
            correct_predictions += 1
    accuracy = (correct_predictions / total_questions) * 100
    return accuracy

if __name__ == "__main__":
    accuracy = validate_model(question_list)
    print(f"Model Accuracy: {accuracy}%")