import json
template = {'target_idx': 1, 'target_pos': 'v', 'predicate_sense': 1}

question_verb_file = 'sample.txt' # input questions here
roleq_input_file = 'input_file.jsonl'
sep = ',' # separator between question and lemma for each line

with open(question_verb_file, 'r') as f:
    lines = f.readlines()

for index, line in enumerate(lines):
    separated = line.strip().split(sep)
    roleq_input = template.copy()
    roleq_input['id'] = index + 1
    roleq_input['sentence'] = separated[0].strip()
    roleq_input['target_lemma'] = separated[1].strip()

    with open(roleq_input_file, 'a') as f:
        json.dump(roleq_input, f)
        f.write('\n')
