import json

question_verb_file = 'cleaned_questions.csv' # input questions here
roleq_input_file = 'input_file_others.jsonl'
sep = ',' # separator between question and lemma and index for each line

keep_preds_file = 'other_preds.txt'
protos = {}
protos["do"] = ["what is something?", "do something?", "something do?"]
protos["be"] = ["what is something?", "what something is?", "what something is something?"]
protos["have"] = ["what does something have?", "what has something?", "what is something's something?"]

keep_preds = set()
with open(keep_preds_file, 'r') as f:
    preds = f.readlines()
    for p in preds:
        keep_preds.add(p.strip())

with open(question_verb_file, 'r') as f:
    lines = f.readlines()

for line in lines:
    separated = line.strip().split(sep)
    roleq_input = {}
    roleq_input['text'] = separated[0].strip()
    lemma = separated[1].strip()

    if lemma not in keep_preds:
        continue

    roleq_input['predicate_lemma'] = lemma

    index = int(separated[2].strip())
    roleq_input['predicate_span'] = f'{index}:{index+1}'


    with open(roleq_input_file, 'a') as f:
        for proto in protos[lemma]:
            roleq_input['proto_question'] = proto 
            json.dump(roleq_input, f)
            f.write('\n')
