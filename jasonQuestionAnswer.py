from Dataset import Dataset # Import the Dataset class from the Dataset.py file
import json

# Define a function to extract information from the dataset based on the questions
def extract_information(dataset, questions):
    results = []
    for question in questions:
        question_text = question['question_text']
        entities = question['entities']
        answers = []

        for data in dataset:
            answer = {}
            for entity in entities:
                entity_answers = []
                suffix = 1
                while f"{entity}_{suffix}" in data:
                    entity_answers.append(data[f"{entity}_{suffix}"])
                    suffix += 1

                if entity_answers:
                    answer[entity] = entity_answers

            if answer:
                answers.append(answer)

        results.append({
            "question": question_text,
            "answers": answers
        })

    return results


# Define a function to save the extracted results to a JSON file
def save_results_to_json(results, filename):
    """Saves the extracted results to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

# Load your dataset
dataset_instance = Dataset('Data/StudyLevelData_Label.csv')
all_data = dataset_instance.get_all_data()

# Define your questions
questions = [
    {"question_text": "What are the names of the authors?", "entities": ["authFull"]},
    {"question_text": "What are the affiliations of the authors?", "entities": ["authAffil"]},
    {"question_text": "What is the title of the paper?", "entities": ["studyID"]}
]

# Extract information based on the questions
results = extract_information(all_data, questions)

# Save the results to a JSON file
save_results_to_json(results, 'extracted_data.json')

# Optionally print out a confirmation or the results
print("Data has been successfully saved to 'extracted_data.json'")



