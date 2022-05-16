from question_translation import QuestionTranslator

model_path = 'contextualizer'
q_translator = QuestionTranslator.from_pretrained(model_path, device_id=0)

samples = [{
        "text": "Lunch was a traditional Brazilian barbecue with different kinds of meat .",
            "proto_question": "what is something?",
                "predicate_lemma": "be",
                    "predicate_span": "1:2",
},{
        "text": "Lunch was a traditional Brazilian barbecue with different kinds of meat .",
            "proto_question": "what something is?",
                "predicate_lemma": "be",
                    "predicate_span": "1:2",
},  {
        "text": "This meeting is part of a new political economy agreement between Brazil and China where Brazil"
                    " has recognized mainland China 's market economy status",
                        "proto_question": "what is something?",
                            "predicate_lemma": "be",
                                "predicate_span": "2:3"
}, {
        "text": "This meeting is part of a new political economy agreement between Brazil and China where Brazil"
                    " has recognized mainland China 's market economy status",
                        "proto_question": "what something is?",
                            "predicate_lemma": "be",
                                "predicate_span": "2:3"
}, {
        "text": "You can buy daily necessities , hardware and so forth in superstores , and the selection is better .",
            "proto_question": "what something is?",
                "predicate_lemma": "be",
                    "predicate_span": "16:17"
}, {
        "text": "You can buy daily necessities , hardware and so forth in superstores , and the selection is better .",
            "proto_question": "what is something?",
                "predicate_lemma": "be",
                    "predicate_span": "16:17"
}, {
        "text": "What is the tenth album of the 21 Pilots?",
            "proto_question": "what is something",
                "predicate_lemma": "is",
                    "predicate_span": "1:2"
}, 
 {
        "text": "What is the tenth album of the 21 Pilots?",
            "proto_question": "who is something",
                "predicate_lemma": "is",
                    "predicate_span": "1:2"
},
{
        "text": "What is the tenth album of the 21 Pilots?",
            "proto_question": "what something is?",
                "predicate_lemma": "is",
                    "predicate_span": "1:2"
}, 
{
        "text": "What is the tenth album of the 21 Pilots?",
            "proto_question": "what something is something?",
                "predicate_lemma": "is",
                    "predicate_span": "1:2"
}, 
{
        "text": "What is the tenth album of the 21 Pilots?",
            "proto_question": "what is something's something?",
                "predicate_lemma": "is",
                    "predicate_span": "1:2"
},
{
        "text": "does the 21 Pilots have a tenth album?",
            "proto_question": "what has something?",
                "predicate_lemma": "have",
                    "predicate_span": "4:5"
},
{
        "text": "does the 21 Pilots have a tenth album?",
            "proto_question": "what does something have?",
                "predicate_lemma": "have",
                    "predicate_span": "4:5"
}, {
        "text": "No one knows if the 21 Pilots has a tenth album.",
            "proto_question": "who has something?",
                "predicate_lemma": "has",
                    "predicate_span": "7:8"
}, {
        "text": "No one knows if the 21 Pilots has a tenth album.",
            "proto_question": "who is something?",
                "predicate_lemma": "has",
                    "predicate_span": "7:8"
}, {
        "text": "No one knows if the 21 Pilots has a tenth album.",
            "proto_question": "does something have something?",
                "predicate_lemma": "has",
                    "predicate_span": "7:8"
}, {
        "text": "No one knows if the 21 Pilots has a tenth album.",
            "proto_question": "who has something?",
                "predicate_lemma": "know",
                    "predicate_span": "2:3"
}, {
        "text": "No one knows if the 21 Pilots has a tenth album.",
            "proto_question": "does something have something?",
                "predicate_lemma": "know",
                    "predicate_span": "2:3"
},{
        "text": "No one knows if the 21 Pilots has a tenth album.",
            "proto_question": "who has something?",
                "predicate_lemma": "know",
                    "predicate_span": "7:8"
}, {
        "text": "No one knows if the 21 Pilots has a tenth album.",
            "proto_question": "does something have something?",
                "predicate_lemma": "know",
                    "predicate_span": "7:8"
}]



fitted_questions = q_translator.predict(samples)
with open('test.txt', 'w') as f:
    f.write('====== Original Questions Below ======\n')
    for i, q in enumerate(fitted_questions):
        if i == 6:
            f.write('====== 21 Pilots Questions Below ======\n')
        f.write(f'{q}\n')
