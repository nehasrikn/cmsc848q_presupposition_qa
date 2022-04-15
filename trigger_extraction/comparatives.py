import spacy
from typing import List, Dict, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class ComparativeExtractor(PresuppositionExtractor):
    """
    Comparative constructions such as Sandy is a bigger cat than Holly 
    take the form X is a W-er Y than Z. The example provided above presupposes 
    that Holly is a cat (i.e., Z is a Y).
    """

    @staticmethod
    def get_trigger_name() -> str:
        return 'comparative'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "That isn't a bigger problem than the chairman's claim."

    @staticmethod
    def find_trigger_instances(sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        triggers = []

        tokens = list(sentence)
        adjs = []
        for token in tokens:  # check the sentence contains an adjective
            if token.pos_ == 'ADJ':
                if str(token.text) not in ["more", "most"]:
                    adjs.append(token)

        for adj in adjs:
            nouns = []
            for word in adj.children:
                if str(word.text) in ["of"]:
                    for word2 in word.children:
                        if word2.dep_ == "pobj" and word2.pos_ == 'NOUN':
                            nouns.append(word2)
            for word in adj.ancestors:
                if word.dep_ == 'attr' and word.pos_ == 'NOUN':
                    nouns.append(word)
            for noun in nouns:  # check if the nouns have 'than' as a prepositional modifier
                for child in noun.children:
                    if child.dep_ == 'prep' and str(child.text) == 'than':
                        triggers.append({
                            'adjective': adj.text,
                            'noun': noun.text,
                            'original_phrase': " ".join(map(str, list([c for c in child.subtree if c != child])))
                        })
        
        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        return '[original_phrase] is a [noun]'

    @staticmethod
    def _presupposition_template_arguments(adjective: str, noun: str, original_phrase: str) -> str:
        return f'{original_phrase} is a {noun}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> str:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(ComparativeExtractor._presupposition_template_arguments(**d))

        return presuppositions

if __name__ == '__main__':
    comparative_extractor = ComparativeExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        #comparative_extractor.get_trigger_canonical_example(),
        "which pyramid is a larger structure than the pyramid of giza"
    ]

    for e in example_sentences:
        print(comparative_extractor.generate_presupposition(nlp(e)))

