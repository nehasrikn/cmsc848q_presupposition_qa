import spacy
from utils import get_dependents_string
from typing import List, Dict, Optional, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class FactiveExtractor(PresuppositionExtractor):
    """
    Clause-embedding predicates frequently presuppose the truth of the finite clause that they embed.
    This set includes verbs such as "realize", "know", and "regret". The sentence "Julia regrets having
    forgotten to feed Holly" presupposes that "it is true that Julia forgot to feed Holly"

    Not all clause-embedding predicates presuppose their complemnt (i.e think or say do not 
    necessarily entail their clausal component).

    The wordlist includes all clause-embedding predicates that appeared in COCA (dataset from NOPE)

    TODO: Include clause-embedding predicates from NQ.
    """

    def __init__(self) -> None:
        self.wordlist = FactiveExtractor.get_wordlist('wordlists/factives.txt')
    
    @staticmethod
    def get_trigger_name() -> str:
        return "factive_clause_embedding_predicate" 

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "We will realize that global warming is important."

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence and the token(s) that caused
        the method to fire.
        """
        triggers = []

        def _check_sentence_for_quote(factive_verb):
            children = [t.text for t in factive_verb.children]
            return "\"" in children or "\'" in children

        factives_in_sentence = [t for t in sentence if t.lemma_ in self.wordlist]
        if len(factives_in_sentence) > 0:
            for factive_verb in factives_in_sentence:
                if _check_sentence_for_quote(factive_verb):
                    continue
                comp_children = [c for c in factive_verb.children if c.dep_ == "ccomp"]
                if len(comp_children) > 0:
                    comp_clause = get_dependents_string(comp_children[0])
                    triggers.append({
                        'factive_verb': str(factive_verb),
                        'comp_clause': str(comp_clause)
                    })
        
        return (True, triggers) if triggers else (False, [])
        

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def _presupposition_template_arguments(factive_verb: str, comp_clause: str) -> str:
        return f'{comp_clause}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(FactiveExtractor._presupposition_template_arguments(**d))

        return presuppositions

    @staticmethod
    def get_wordlist(wordlist_path: str) -> Optional[List[str]]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]

if __name__ == '__main__':
    factive_extractor = FactiveExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        factive_extractor.get_trigger_canonical_example(),
    ]

    for e in example_sentences:
        print(factive_extractor.generate_presupposition(nlp(e)))

