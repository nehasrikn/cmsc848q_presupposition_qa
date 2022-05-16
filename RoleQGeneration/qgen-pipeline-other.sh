# Don't forget to modify the following 2 variables inside roleq-input-others.py
# question_verb_file (file of all questions, verbs, and indices)
# sep (separates question, verb, and predicate index)

rm input_file_others.jsonl
python roleq-input-others.py 
python roleq-output-others.py
