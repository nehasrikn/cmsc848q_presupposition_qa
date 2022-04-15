import spacy
from typing import List, Optional, Dict, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class ContinuationOfStateExtractor(PresuppositionExtractor):
    """
    Aspectual verbs such as "start" and "stop" presuppose whether the event
    that is embedded under these verbs had previously been happening or not.
    The sentence "Lisa stopped petting Tom's cat" presupposes that "Lisa
    had previously been petting Tom's cat". Aspectual verbs are 
    frequently subsumed under change of state verbs, but unlike the verbs
    we consider change of state verbs, aspectual verbs take a non-finite 
    verb phrase (e.g. "petting Tom's cat" or "to eat the kibble") as a 
    complement.
    """

    def __init__(self) -> None:
        self.wordlist = ContinuationOfStateExtractor.get_wordlist('wordlists/continuation_of_state.txt')

    @staticmethod
    def get_trigger_name() -> str:
        return 'continuation_of_state'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "At the age of 16, I began preparing myself for college."

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        triggers = []

        words = [t.text for t in sentence]
    
        if set(words) & set(self.wordlist): 
            for token in sentence: 
                if (str(token)) in self.wordlist and token.tag_[0] == "V" and token.dep_ == "ROOT": 
                    for child in token.children: 
                        if child.dep_ in ["xcomp", "ccomp"]:
                            triggers.append({
                                'subject': str([c for c in token.children if 'subj' in c.dep_][0]),
                                'continuation_of_state_predicate': str(token),
                                'modified_phrase': " ".join(map(str, list(child.subtree)))
                            }) 

        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def _presupposition_template_arguments(subject: str, continuation_of_state_predicate: str, modified_phrase: str) -> str:
        return f'{subject} had not previously been {modified_phrase}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(ContinuationOfStateExtractor._presupposition_template_arguments(**d))

        return presuppositions

    @staticmethod
    def get_wordlist(wordlist_path: str) -> Optional[List[str]]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]

if __name__ == '__main__':
    continuation_of_state_extractor = ContinuationOfStateExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        continuation_of_state_extractor.get_trigger_canonical_example(),
        "when did the nfl start playing the national anthem"
    ]

    for e in example_sentences:
        print(continuation_of_state_extractor.generate_presupposition(nlp(e)))
