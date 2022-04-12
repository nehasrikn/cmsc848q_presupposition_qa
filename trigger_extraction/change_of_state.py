import spacy
from typing import List, Optional, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class ChangeOfStateExtractor(PresuppositionExtractor):
    """
    Change of state verbs such as 'appear' or 'snap'
    presuppose that the entity that was affected by the
    described event was in a different state just before the event
    happened. For instance, the sentence "Cats appeared on the street"
    presupposes that "cats had not been on the street right before then".
    """

    def __init__(self) -> None:
        self.wordlist = ChangeOfStateExtractor.get_wordlist('wordlists/change_of_state.txt')

    @staticmethod
    def get_trigger_name() -> str:
        raise 'change_of_state'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "A microsecond later, images from his exterior sensors snapped \
            into focus."

    def find_trigger(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[str]]:
        """
        Returns whether or not trigger is found in sentence.
        Conditions: If there exists a token that is in the wordlist, and is a verb, and is the
        root of the dependency parse, this method will fire.
        """
        for token in sentence: 
            if (token.lemma_ in self.wordlist) and token.tag_[0] == "V" and token.dep_ == "ROOT":
                return (True, [token])
        return (False, None)

    @staticmethod
    def presupposition_template() -> str:
        return "were not there before"

    @staticmethod
    def generate_presupposition(sentence: str) -> str:
        raise NotImplementedError

    @staticmethod
    def get_wordlist(wordlist_path: str) -> List[str]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]


if __name__ == '__main__':
    change_of_state_extractor = ChangeOfStateExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    print(change_of_state_extractor.find_trigger(
        nlp(change_of_state_extractor.get_trigger_canonical_example()))
    )

