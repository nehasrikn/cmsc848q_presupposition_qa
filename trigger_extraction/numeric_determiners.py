import spacy
from typing import List, Optional, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class NumericDeterminerExtractor(PresuppositionExtractor):
    """
    Numeric determiners such as "both" or "all" X, where X is a numeric 
    expression such as "three" presuppose that there is a precise 
    number of modified entities in the context. The sentence
    "All three cat owners that Julia spoke to want another cat"
    presupposes that "there are three cat owners that Julia spoke to". 
    Extracted sentences contain "both (of the) N", "all NUM (of the) N", 
    or "all (of the) NUM N" where N is a noun with optional modifiers, 
    and NUM is a numeric expression.
    """

    NUMERIC_PREDETERMINERS = set(["all"])
    SPECIAL_DETERMINERS = set(["both"])
    ALL_DETERMINERS = NUMERIC_PREDETERMINERS | SPECIAL_DETERMINERS

    @staticmethod
    def get_trigger_name() -> str:
        raise 'numeric_determiner'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "Both protagonists in the room defy a political force and receive aid from a higher authority."

    def find_trigger(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[str]]:
        words = [t.text.lower() for t in sentence]
        
        if set(words) & NumericDeterminerExtractor.ALL_DETERMINERS:
            for token in sentence:
                include = False
                if token.text.lower() in NumericDeterminerExtractor.SPECIAL_DETERMINERS:
                    if token.tag_ == "DT" and token.dep_ == "det":
                        include = True
                        return (True, [token])  
                    if not include:
                        for child in token.children:
                            if child.dep_ == "prep" and child.text.lower() == "of":
                                include = True
                                return (True, [token]) 

            if not include and token.text.lower() in NumericDeterminerExtractor.NUMERIC_PREDETERMINERS:
                if token.tag_ == "DT" and token.dep_ == "det":
                    head_token = token.head
                    if head_token.tag_ == "CD":
                        include = True # all three of the children
                        return (True, [token])  
                    else:
                        for child in head_token.children:
                            if child.tag_ == "CD" and child.dep_ == "nummod":  ## changed token.dep_ to child.dep_ 
                                include = True # all three children
                                return (True, [token]) 
                
                elif token.tag_ == "DT":
                    for child in token.children:
                        if child.dep_ == "prep" and child.text.lower() == "of":
                            for child_child in child.children:
                                if child_child.dep_ == "pobj":
                                    has_det = False
                                    has_nummod = False
                                    for child_child_child in child_child.children:
                                        if (child_child_child.tag_ == "CD"
                                            and child_child_child.dep_ == "nummod"):
                                            has_nummod = True # all of the three children
                                        if (child_child_child.tag_ == "DT"
                                            and child_child_child.dep_ == "det"):
                                            has_det = True # all of the three children

                                    include = has_det and has_nummod
                                    if include:
                                        return (True, [token]) 
                            if include:
                                return (True, [token]) 
        return (False, [])

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def generate_presupposition(sentence: str) -> str:
        raise NotImplementedError


if __name__ == '__main__':
    numeric_determiner_extractor = NumericDeterminerExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    print(numeric_determiner_extractor.find_trigger(
        nlp(numeric_determiner_extractor.get_trigger_canonical_example()))
    )

