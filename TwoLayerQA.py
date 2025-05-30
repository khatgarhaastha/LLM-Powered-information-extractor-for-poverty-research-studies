
from config import *
from utils import *
import jinja2
import json
import requests

# Define the entity for which we want 2 layer QA
ENTITY = 'interventions'

# get the location of base questions JSON from entity
BASE_QUESTIONS_JSON = ENTITY_QUESTION_MAPPING[ENTITY]

# Define the location of the PDF file here
pdf_file_path = SAMPLE_PDF_LOCATION

# Extract Text from PDF 
_, processed_text_data = extract_data_from_pdf(pdf_file_path)

# Load the base questions from JSON file
with open(BASE_QUESTIONS_JSON, 'r', encoding='utf-8') as file:
    base_questions = json.load(file)

# Send Prompt to LLM for first layer of QA
prompt = jinja2.Template(BASE_TEMPLATE).render(research_paper=processed_text_data, questions=base_questions)

# Call LLM
url = LLM_API_URL
data = {"model": "llama3.1", "prompt": prompt, "stream": False}
entity_information = json.loads(requests.post(url, json=data).content.decode('utf-8'))['response']

# Define the location of stage 2 questions JSON from entity
STAGE2_QUESTIONS_JSON = ENTITY_STAGE2_QUESTION_MAPPING[ENTITY]

# Load the stage 2 questions from JSON file
with open(STAGE2_QUESTIONS_JSON, 'r', encoding='utf-8') as file:
    stage2_questions = json.load(file)

# Send Prompt to LLM for second layer of QA
prompt = jinja2.Template(STAGE2_TEMPLATE).render(research_paper=processed_text_data, questions=stage2_questions, var_name=ENTITY, entities=entity_information)

# Call LLM
data = {"model": "llama3.1", "prompt": prompt, "stream": False}
final_response = json.loads(requests.post(url, json=data).content.decode('utf-8'))['response']

print(final_response)


'''
{{research_paper}}

{{var_name}} mentioned in the paper : 
{{entities}}


Here are the questions you have to answer based on information from the research paper : 
{{questions}}
'''