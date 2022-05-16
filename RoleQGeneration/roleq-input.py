import json
template = {'target_pos': 'v', 'predicate_sense': 1}

question_verb_file = 'cleaned_questions.csv' # input questions here
roleq_input_file = 'input_file.jsonl'
sep = ',' # separator between question and lemma and index for each line

ignore_preds_file = 'other_preds.txt'

ignore_preds = set()
with open(ignore_preds_file, 'r') as f:
    preds = f.readlines()
    for p in preds:
        ignore_preds.add(p.strip())

with open(question_verb_file, 'r') as f:
    lines = f.readlines()

for index, line in enumerate(lines):
    separated = line.strip().split(sep)
    roleq_input = template.copy()
    roleq_input['id'] = index + 1
    roleq_input['sentence'] = separated[0].strip()
    roleq_input['target_lemma'] = separated[1].strip()
    roleq_input['target_idx'] = int(separated[2].strip())

    if roleq_input['target_lemma'] in ignore_preds:
        continue

    with open(roleq_input_file, 'a') as f:
        json.dump(roleq_input, f)
        f.write('\n')
