from utils import * 
from config import *
import jinja2
import requests
import json

def prepare_table_prompt(table, questions):

    #Render the J2 template
    with open(TABLE_TEMPLATE_LOCATION, 'r', encoding="utf") as file:
        template = file.read()
    
    prompt = jinja2.Template(template).render(table=table, questions=questions)

    return prompt



def test():
    pdf_path = 'C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Data/DeMel2013.pdf'

    # Extract tables from PDF 
    tables = extract_tables(pdf_path)
 
    # Gather the questions from JSON file
    question_json = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Phase2/questions/tableQuestions.json"
    with open(question_json, 'r', encoding='utf-8') as file:
        questions = json.load(file)


    # Extract question answers from each table 
    answers = []

    for i, table in enumerate(tables):
        print(f"Extracting answers from table {i+1}")
        prompt = prepare_table_prompt(table, questions)
        response = call_LLM(prompt)
        print(response)
        answers.append((table.to_dict(orient='records'), response))

    # Save the answers to a file
    with open('C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Phase2/table_answers.json', 'w') as file:
        json.dump(answers, file, indent=4)
if __name__ == '__main__':
    test()