import spacy
from typing import List, Optional, Tuple
from base_presupposition_extractor import PresuppositionExtractor
from utils import get_dependents_string


class EmbeddedQuestionExtractor(PresuppositionExtractor):
    """
    Embedded questions are realized when a clause is embedded under a wh-word such as
    "why", "how", "where", or "when" as in "Julia knows why Lisa likes Tom's cat".
    These triggers presuppose the truth of the embedded content; the example provided
    above presupposes that "Lisa likes Tom's cat."
    """

    PRESUPPOSITIONAL_WH_WORDS = ["why", "how", "where", "when", "who", "what", "which"]

    def __init__(self) -> None:
        self.wordlist = EmbeddedQuestionExtractor.get_wordlist('wordlists/embedded_question.txt')
        self.wh_predicates_1_word = [l.split()[0] for l in self.wordlist]

    @staticmethod
    def get_trigger_name() -> str:
        return 'embedded_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "I fail to see how you could rationalize rewarding illegality."

    def find_trigger(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[str]]:
        """
        Returns whether or not trigger is found in sentence, and
        preposition and embedded clause head tag if found.
        """
        def _check_sentence_for_quote(verb):
            children = [t.text for t in verb.children]
            return "\"" in children or "\'" in children
        
        if len([wh for wh in self.wordlist if wh in sentence.text]) > 0:    # are there wh predicates in the sentence?
            wh_predicates_in_sentence = [t for t in sentence if t.lemma_.lower() in self.wh_predicates_1_word]
            
            for wh_predicate in wh_predicates_in_sentence:     # do any of the wh predicates actually have a wh-clause
                if _check_sentence_for_quote(wh_predicate):
                    continue
                ccomp_children = [c for c in wh_predicate.children if c.dep_ == "ccomp"]
                if len(ccomp_children) > 0:   # NOTE: You could exclude sentences with embedded clauses inside the complement clause, to make judgments simpler
                    for c in ccomp_children:  # is the embedded clause interrogative?
                        try:
                            if next(c.children).text in EmbeddedQuestionExtractor.PRESUPPOSITIONAL_WH_WORDS:
                                embedded_q = get_dependents_string(c)
                                return (True, [wh_predicate, embedded_q])
                        except Exception:
                            continue
        return (False, [])


    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def generate_presupposition(sentence: str) -> str:
        raise NotImplementedError


    @staticmethod
    def get_wordlist(wordlist_path: str) -> List[str]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]


if __name__ == '__main__':
    embedded_question_extractor = EmbeddedQuestionExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    print(embedded_question_extractor.find_trigger(
        nlp("Which means , throw something up and you know exactly where it will fall to moon again."))
    )

