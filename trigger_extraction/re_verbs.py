import spacy
from typing import List, Dict, Optional, Tuple
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

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        triggers = []

        words = [t.text for t in sentence]
    
        if set(words) & set(self.wordlist):
            for token in sentence:
                if (str(token) in self.wordlist and token.tag_[0] == "V" and token.dep_ == "ROOT"):
                    if len(list(token.children))  > 0: 
                        triggers.append({
                            're_verb': str(token)
                        })
        

        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def _presupposition_template_arguments(re_verb: str) -> str:
        return f'{re_verb}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(RePrefixedVerbExtractor._presupposition_template_arguments(**d))

        return presuppositions

    @staticmethod
    def get_wordlist(wordlist_path: str) -> List[str]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]


if __name__ == '__main__':
    re_prefixed_verb_extractor = RePrefixedVerbExtractor()
    
    nlp = spacy.load("en_core_web_sm")


    example_sentences = [
        re_prefixed_verb_extractor.get_trigger_canonical_example(),
        "Kim finally resurfaces.",
        "Six weeks after the Jenkins died, the hotel reopened Room 225."
    ]

    for e in example_sentences:
        print(re_prefixed_verb_extractor.generate_presupposition(nlp(e)))

