import spacy
from typing import List, Optional, Tuple
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
    def find_trigger(sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[str]]:
        """
        Returns whether or not trigger is found in sentence.
        """
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
                        return (True, [adj.text, noun.text])
        
        return (False, [])

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def generate_presupposition(sentence: str) -> str:
        raise NotImplementedError

if __name__ == '__main__':
    comparative_extractor = ComparativeExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    print(comparative_extractor.find_trigger(
        nlp(comparative_extractor.get_trigger_canonical_example()))
    )
