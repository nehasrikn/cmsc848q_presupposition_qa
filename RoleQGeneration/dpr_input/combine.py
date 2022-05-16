import json

files = ['cleaned_gen_questions.json', 'cleaned_gen_questions_others.json']
out_file = 'all_dpr_questions.txt'

all_questions = []
for json_file in files:
    with open(json_file, 'r') as f:
        curr_json = json.load(f)
        for _, v in curr_json.items():
            all_questions.extend(v)


with open(out_file, 'w') as f:
    f.write('\n'.join(all_questions))
