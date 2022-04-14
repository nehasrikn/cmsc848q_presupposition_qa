import spacy
from typing import List, Optional, Dict, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class PossessiveExtractor(PresuppositionExtractor):
    """
    """

    @staticmethod
    def get_trigger_name() -> str:
        return 'possessive'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "what was the relationship between japan’s emperors and military leaders?"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, Optional[List[Dict[str, str]]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        triggers = []

        for token in sentence: 
            if token.tag_ == "POS": 
                direct_head = token.head
                possessive_subtree = list(direct_head.head.subtree)
                subtree_tags = [t.tag_ for t in possessive_subtree]

                pos_index = subtree_tags.index('POS')

                triggers.append({
                    'head': " ".join(map(str, possessive_subtree[:pos_index])),
                    'possessive_phrase': " ".join(map(str, possessive_subtree[pos_index+1:]))
                })

        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        return '[head] has [possessive_phrase]'

    @staticmethod
    def _presupposition_template_arguments(head: str, possessive_phrase: str) -> str:
        return f'{head} has {possessive_phrase}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(PossessiveExtractor._presupposition_template_arguments(**d))

        return presuppositions



if __name__ == '__main__':
    possessive_extractor = PossessiveExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    print(possessive_extractor.find_trigger_instances(
        nlp(possessive_extractor.get_trigger_canonical_example()))
    )
    print(possessive_extractor.generate_presupposition(nlp(possessive_extractor.get_trigger_canonical_example())))

