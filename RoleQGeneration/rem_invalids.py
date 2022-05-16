import json

files = ['gen_questions.json', 'gen_questions_others.json']


for json_file in files:
    with open(json_file, 'r') as f:
        curr_json = json.load(f)
        for k, v in curr_json.items():
           curr_json[k] = [question for question in v if question != 'No Prototype'] 

    with open(f'cleaned_{json_file}', 'w') as f:
        json.dump(curr_json, f)
