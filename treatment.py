from utils import *
from config import *
import jinja2
import requests
import json



def treatment_extraction(pdf_path):
        # Define PDF path here 
        PDF_PATH = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Data/DeMel2013.pdf"
        TEMPLATE_PATH = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Phase2/template/describe_treatments.j2"
        ENTITY = 'interventions'

        # Convert PDF to text 
        _, processed_text_data = extract_data_from_pdf(PDF_PATH)

        print(f'The length of encoded PDF is {len(json.dumps(processed_text_data))}')
        # Prepare the prompt for the LLM : load text into the prompt 
        with open(TEMPLATE_PATH, 'r', encoding="utf") as file:
                template = file.read()
        prompt = jinja2.Template(template).render(research_paper=processed_text_data)
        #print(prompt)
        # Call the LLM
        entity_data = call_LLM(prompt)

        # Print the response
        print(f'The details of {ENTITY} is as follows :\n{entity_data}')

        # Second layer of questions Starts here 

        # Load the questions for layer 2 : 
        second_layer_questions = ENTITY_STAGE2_QUESTION_MAPPING[ENTITY]

        second_layer_questions = json.load(open(second_layer_questions, 'r', encoding='utf-8'))

        # Read SecondL.j2 file and load second prompt
        TEMPLATE_PATH = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Phase2/template/SecondL.j2"
        with open(TEMPLATE_PATH, 'r', encoding="utf") as file:
                template = file.read()

        prompt = jinja2.Template(template).render(research_paper=processed_text_data, var_name = ENTITY, entities = entity_data, questions = second_layer_questions)

        # Call the LLM
        Intervention_level_details = call_GPT(prompt)

        # Print the response
        print(f' The {ENTITY} Overall Questions are answered as follows:\n{Intervention_level_details}')

        # lOAN QUESTIONS 
        # Load the questions for layer 2 :
        loan_questions = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Phase2/questions/treatmentModules.json"
        loan_questions = json.load(open(loan_questions, 'r', encoding='utf-8'))

        # Read SecondL.j2 file and load second prompt
        TEMPLATE_PATH = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Phase2/template/SecondL.j2"
        with open(TEMPLATE_PATH, 'r', encoding="utf") as file:
                template = file.read()

        prompt = jinja2.Template(template).render(research_paper=processed_text_data, var_name = ENTITY, entities = entity_data, questions = loan_questions)

        # Call the LLM
        loan_module_data = call_GPT(prompt)

        # Print the response
        print(f'The Loan Module Details are as follows : {loan_module_data}')


        # Load questions for Business Training Module : 

        loan_questions = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Data/Phase2/TrainingModule.json"
        loan_questions = json.load(open(loan_questions, 'r', encoding='utf-8'))

        # Read SecondL.j2 file and load second prompt
        TEMPLATE_PATH = "C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Phase2/template/SecondL.j2"
        with open(TEMPLATE_PATH, 'r', encoding="utf") as file:
                template = file.read()

        prompt = jinja2.Template(template).render(research_paper=processed_text_data, var_name = ENTITY, entities = entity_data, questions = loan_questions)

        # Call the LLM
        business_training_module = call_GPT(prompt)

        # Print the response
        print(f'The Business Trainign module details are as follows : {business_training_module}')

        return {"interventions": entity_data, "Intervention_level_details": Intervention_level_details, "loan_module_data": loan_module_data, "business_training_module": business_training_module}



