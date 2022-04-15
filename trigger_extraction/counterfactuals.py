import spacy
from typing import List, Optional, Dict, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class CounterfactualExtractor(PresuppositionExtractor):
    """
    Counterfactuals (if+ past):I would have been happier if I had a dog. » I don’t have a dog.
    """

    @staticmethod
    def get_trigger_name() -> str:
        return 'counterfactual'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "who would have been president if the south won the civil war"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        triggers = []

        for token in sentence:
            if token.tag_ == 'IN' and str(token).lower() == 'if':
                head = token.head
                triggers.append({
                    'counterfactual_phrase': " ".join(
                        [str(t) for t in head.subtree if t != token and t.dep_ not in ('punct')]
                    )
                })

        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        return 'it is not true that [counterfactual_phrase]'

    @staticmethod
    def _presupposition_template_arguments(counterfactual_phrase: str) -> str:
        return f'it is not true that {counterfactual_phrase}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(CounterfactualExtractor._presupposition_template_arguments(**d))

        return presuppositions


if __name__ == '__main__':
    counterfactual_extractor = CounterfactualExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        counterfactual_extractor.get_trigger_canonical_example(),
        "who will be the next in line if vice mayor dies",
        "where would you go if freedom of speech is denied to you",

    ]

    for e in example_sentences:
        print(counterfactual_extractor.generate_presupposition(nlp(e)))

