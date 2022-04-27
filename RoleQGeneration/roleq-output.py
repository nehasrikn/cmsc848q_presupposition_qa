import json

roleq_output = 'output_file.jsonl'
qgen_output = 'gen_questions.json'
qgen = {}

with open(roleq_output, 'r') as f:
    for line in f:
        curr_json = json.loads(line)
        question = curr_json['sentence']
        gen = []
        if type(curr_json['questions']) is dict:
            gen += list(curr_json['questions'].values())
        if type(curr_json['adjunct_questions']) is dict:
            gen += list(curr_json['adjunct_questions'].values())

        prev_gen = qgen.get(question, [])
        qgen[question] = prev_gen + gen


with open(qgen_output, 'w') as f:
    json.dump(qgen, f)
