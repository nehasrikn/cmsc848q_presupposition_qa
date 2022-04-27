# Don't forget to modify the following 2 variables inside roleq-input.py
# question_verb_file (file of all questions and verbs)
# sep (separates question from verb)

python roleq-input.py # takes input file of questions separated with verbs and outputs input file for roleq model
bash pred.sh # generates questions using previously generated input file
python roleq-output.py # takes output file and merges all sentences with their generated questions into gen_questions.json
