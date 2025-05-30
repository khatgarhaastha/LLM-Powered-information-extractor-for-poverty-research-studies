import os 
import json

perTokenChar = 4
total_tokens = 165000 

def convert_JSON_to_string(json_data) -> str:
    
    # Convert the json_data to a string and return the string
    return json.dumps(json_data)

def calculate_token_count(text):
    return len(text) // perTokenChar

def get_question_entity_mapping(json_file_path) -> dict:
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return data

def token_overview():
    # Read the text from the file
    base_path = "Data/Processed/"
    for files in os.listdir(base_path):
        if files.endswith(".txt"):
            with open(base_path + files, "r", encoding = "utf") as file:
                raw_text_data = file.read()
            
            token_count = calculate_token_count(raw_text_data)
            print(f"File: {files} has {token_count} tokens")

def tokens_from_questions():
    question_data = get_question_entity_mapping("Data/Questions/questions.json")
    data = convert_JSON_to_string(question_data)
    token_count = calculate_token_count(data)
    print(f"Questions have {token_count} tokens")

def setupAPICall(data, questions, total_tokens = 165000):
    data_tokens = calculate_token_count(data)

    tokens_for_questions = total_tokens - data_tokens
    api_call = 1

    question_batch = []
    current = []
    current_token_count = 0
    questionList = questions["Questions"]

    for question in questionList:
        question_string = convert_JSON_to_string(question)
        question_tokens = calculate_token_count(question_string)

        if current_token_count + question_tokens <= tokens_for_questions:
            current.append(question)
            current_token_count += question_tokens
        else:
            question_batch.append(current)
            current = [question]
            current_token_count = question_tokens
            api_call += 1
    
    question_batch.append(current)
    return question_batch, api_call


def batch_from_jsons(path):
    api_call = 1
    question_batch = []
    

    for files in os.listdir(path):
        if files.endswith(".json"):
            current = []
            with open(path + files, "r", encoding="utf") as file:
                data = json.load(file)

            questionList = data["Questions"]
            for question in questionList:
                current.append(question)
            question_batch.append(current)
            api_call += 1

    return question_batch, api_call

if __name__ == '__main__':
    token_overview()
    tokens_from_questions()
    question_data = get_question_entity_mapping("Data/Questions/questions.json")
    data = convert_JSON_to_string(question_data)
    batched_questions, api_calls = batch_from_jsons("Data/Questions/")
    print(api_calls)



