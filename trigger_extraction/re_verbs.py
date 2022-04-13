import spacy
from typing import List, Optional, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class RePrefixedVerbExtractor(PresuppositionExtractor):
    """
    Verbs with the prefix re- presuppose that the action of 
    the verb (attaching to re-) had taken place in the past. The sentence 
    "Holly re-entered the room" presupposes that "Holly had entered the room before".  
    Hence, re-V presupposes that V had been carried out before.
    """

    def __init__(self) -> None:
        # TODO: what's the difference between re_verbs_updated and re_verbs in the NOPE code?
        # TODO: Why does the example "Holly decided to re-book the flight." not work?

        self.wordlist = RePrefixedVerbExtractor.get_wordlist('wordlists/re_verbs.txt')

    @staticmethod
    def get_trigger_name() -> str:
        return 're_prefixed_verbs'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "Taoism reconnects aging to the great cycles of nature."

    def find_trigger(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[str]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        words = [t.text for t in sentence]
    
        if set(words) & set(self.wordlist):
            for token in sentence:
                if (str(token) in self.wordlist and token.tag_[0] == "V" and token.dep_ == "ROOT"):
                    if len(list(token.children))  > 0: 
                        return (True, [token]) 
        return (False, [])

    @staticmethod
    def presupposition_template() -> str:
        return "happened before"

    @staticmethod
    def generate_presupposition(sentence: str) -> str:
        raise NotImplementedError

    @staticmethod
    def get_wordlist(wordlist_path: str) -> List[str]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]


if __name__ == '__main__':
    re_prefixed_verb_extractor = RePrefixedVerbExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    print(re_prefixed_verb_extractor.find_trigger(
        nlp(re_prefixed_verb_extractor.get_trigger_canonical_example()))
    )

