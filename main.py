from utils import extract_data_from_pdf
import jinja2
import requests
import json



if __name__ == '__main__':
    
    # Define the location of the PDF file here
    pdf_file_path = 'C:/Users/Bhavin/Desktop/work/Practicum/DataEntry/data_entry/Data/DeMel2013.pdf'
    _, processed_text_data = extract_data_from_pdf(pdf_file_path)


    # Define Template Location here : 
    template_location = ""
    with open(template_location, 'r', encoding="utf") as file:
        template = file.read()

    '''
    __.render(first_var_to_pass = first_var, second_var_to_pass = second_var, ...)

    To define the variables to pass to the template, you can use the following format in template : 
    let's say you want to pass a variable named research_paper to the template, you can use the following format in the template :
        
        {{ research_paper }}

    '''
    prompt = jinja2.Template(template).render(research_paper=processed_text_data, questions=None)


    url = 'http://localhost:11434/api/generate'
    data = {"model": "llama3.1", "prompt": prompt, "stream": False}
    response = json.loads(requests.post(url, json=data).content.decode('utf-8'))['response']

    print(response)