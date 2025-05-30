import requests
import json

def test():
    url = "http://localhost:8000/get_answer/"
    
    # read txt file 
    with open('Data/Processed/ExtractedText_Brun.txt', 'r', encoding="utf") as file:
        rawtext = file.read()
    # read a json file
    with open('Data/groupedQuestions/authorship_details.json', 'r') as file:
        questions = json.load(file)

    data = {}

    data["rawtext"] = rawtext
    data["questions"] = questions["Questions"]

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)

if __name__ == "__main__":
    test()