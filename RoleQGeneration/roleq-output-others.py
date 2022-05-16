import json
from question_translation import QuestionTranslator

model_path = 'contextualizer'
q_translator = QuestionTranslator.from_pretrained(model_path, device_id=0)
data_file = 'input_file_others.jsonl'
qgen_output = 'gen_questions_others.json'

with open(data_file) as f:
    json_list = list(f)

questions = []
data = []
for json_str in json_list:
    curr_json = json.loads(json_str)
    questions.append(curr_json['text'])
    data.append(curr_json)


fitted_questions = q_translator.predict(data)

qgen = {}
for q, next_q in zip(questions, fitted_questions):
    prev_gen = qgen.get(q, [])

    qgen[q] = prev_gen + [next_q]


with open(qgen_output, 'w') as f:
    json.dump(qgen, f)
