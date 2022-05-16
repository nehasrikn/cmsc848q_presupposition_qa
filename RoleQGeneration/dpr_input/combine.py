import json

files = ['cleaned_gen_questions.json', 'cleaned_gen_questions_others.json']
out_file = 'all_dpr_questions.txt'
linked_out_file = 'all_dpr_questions_linked.txt'

all_questions = set()
linked_questions = set()
for json_file in files:
    with open(json_file, 'r') as f:
        curr_json = json.load(f)
        for k, v in curr_json.items():
            for question in v:
                all_questions.add(question.strip())
                linked_questions.add(f'{k.strip()},{question.strip()}')


with open(out_file, 'w') as f:
    f.write('\n'.join(all_questions))


with open(linked_out_file, 'w') as f:
    sorted_linked = sorted(list(linked_questions))
    f.write('\n'.join(sorted_linked))
