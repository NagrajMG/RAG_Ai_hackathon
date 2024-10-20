import json
import pathlib

def jsonl_to_question_list(file_path):
    questions_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            question_data = json.loads(line)
            question_entry = {
                "question": question_data["question"],
                "options": question_data["options"],
                "answer_idx": question_data["answer_idx"]
            }
            questions_list.append(question_entry)
    print("done")
    return questions_list

root_dir = pathlib.Path(__file__).parent
folder_path=str(root_dir /'questions'/'US' /'4_options' / 'phrases_no_exclude_dev.jsonl')

question_list = jsonl_to_question_list(folder_path)
print(question_list[0], question_list[1], question_list[2], question_list[3])