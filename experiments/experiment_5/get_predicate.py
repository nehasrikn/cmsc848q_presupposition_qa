import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def find_predicate(sent):
    is_verb = lambda tok: tok.pos_.startswith('V') or tok.pos_.startswith('AUX')
    root = list(filter(lambda tok: tok.dep_ == 'ROOT', sent))[0]            
    if is_verb(root):
        return str(root.lemma_)
    else:
        for tok in root.children:
            if is_verb:
                return str(tok.lemma_)
    return None


questions = pd.read_csv('../../datasets/linguist_lightbulb_unanswerable_analysis_for_agreement_for_sharing.tsv', sep='\t')
questions['predicate'] = questions.question.map(lambda x: find_predicate(nlp(x)))
questions[['question', 'document', 'predicate']].to_csv('./experiments/experiment_5/linguist_lightbulb_questions_with_predicates.csv', index=False)