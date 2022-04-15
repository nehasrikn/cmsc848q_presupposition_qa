import spacy
from typing import List, Dict, Optional, Tuple
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
        return 'change_of_state'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "A microsecond later, images from his exterior sensors snapped \
            into focus and filled the screen."

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, Optional[List[Dict[str, str]]]]:
        """
        Returns whether or not trigger is found in sentence.
        Conditions: If there exists a token that is in the wordlist, and is a verb, and is the
        root of the dependency parse, this method will fire.
        """
        triggers = []

        for token in sentence: 
            if (token.lemma_ in self.wordlist) and token.tag_[0] == "V" and token.dep_ == "ROOT":
                triggers.append({'change_of_state_predicate': token})
        
        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        return "not [change_of_state_predicate] before"

    @staticmethod
    def _presupposition_template_arguments(change_of_state_predicate: str) -> str:
        return f'not {change_of_state_predicate} before'

    def generate_presupposition(self, sentence: str) -> str:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(ChangeOfStateExtractor._presupposition_template_arguments(**d))

        return presuppositions

    @staticmethod
    def get_wordlist(wordlist_path: str) -> List[str]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]


if __name__ == '__main__':
    change_of_state_extractor = ChangeOfStateExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        change_of_state_extractor.get_trigger_canonical_example(),
    ]

    for e in example_sentences:
        print(change_of_state_extractor.generate_presupposition(nlp(e)))

