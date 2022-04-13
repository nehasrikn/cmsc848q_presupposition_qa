import spacy
from typing import List, Optional, Tuple
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
        raise 'continuation_of_state'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "At the age of 16, I began preparing myself for college."

    def find_trigger(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, Optional[List[str]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        words = [t.text for t in sentence]
    
        if set(words) & set(self.wordlist): 
            for token in sentence: 
                if (str(token)) in self.wordlist and token.tag_[0] == "V" and token.dep_ == "ROOT": 
                    for child in token.children: 
                        if child.dep_ in ["xcomp", "ccomp"]: 
                            return (True, [token]) 

        return (False, []) 

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def generate_presupposition(sentence: str) -> str:
        raise NotImplementedError

    @staticmethod
    def get_wordlist(wordlist_path: str) -> Optional[List[str]]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]

if __name__ == '__main__':
    continuation_of_state_extractor = ContinuationOfStateExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    print(continuation_of_state_extractor.find_trigger(
        nlp(continuation_of_state_extractor.get_trigger_canonical_example()))
    )
