import spacy
from spacy import displacy
from spacy.matcher import PhraseMatcher
from typing import List, Dict, Optional, Tuple, Set
from base_presupposition_extractor import PresuppositionExtractor


class ImplicativeExtractor(PresuppositionExtractor):
    """
    Implicative  verbs  such as "manage to" and "fail to" presuppose some property 
    of the action in the clause that they embed. For example, the sentence "Holly failed to escape 
    her pet taxi" presupposes that "Holly attempted to escape her pet taxi", since "fail to" 
    implies an attempt at the action. Likewise, "Holly managed to X" presupposes that
    "X would take effort for Holly".
    """

    def __init__(self) -> None:
        self.matcher, self.wordlist, self.implicative_inferences_dict = self._process_wordlist(
            ImplicativeExtractor.get_wordlist('wordlists/implicatives.txt')
        )

    @staticmethod
    def get_trigger_name() -> str:
        return 'implicative'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "The survivors managed to scramble out through the tiny gap in the rocks."

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        triggers = []

        matches = self.matcher(sentence)
        if len(matches) > 0:
            for match_id, start, end in matches:
                impl_phrase = sentence[start:end]
            # match found, proceed to further checking
            for token in sentence:
                if (str(token) in self.wordlist and token.tag_[0] == "V" and token.dep_ == "ROOT"):
                    for child in token.children:
                        if child.dep_ == "prep":
                            for childs in child.children:
                                if childs.dep_ == "pcomp" and childs.pos_ == "VERB":
                                    triggers.append({
                                        'action': str(childs),
                                        'implicative_verb': str(token),
                                        'inference': self.implicative_inferences_dict[str(token)]
                                    })
                        else:
                            if child.dep_ == "xcomp" and child.pos_ == "VERB":
                                triggers.append({
                                    'action': str(child),
                                    'implicative_verb': str(token),
                                    'inference': self.implicative_inferences_dict[str(token)]
                                })
        return (True, triggers) if triggers else (False, [])  

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def _presupposition_template_arguments(action: str, implicative_verb: str, inference: str) -> str:
        return f'{action} -> {inference}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(ImplicativeExtractor._presupposition_template_arguments(**d))

        return presuppositions

    @staticmethod
    def get_wordlist(wordlist_path: str) -> List[str]:
        with open(wordlist_path) as f: 
            return [l.strip() for l in f.readlines()]

    def _process_wordlist(self, wordlist: List[str]) -> Tuple[PhraseMatcher, Set[str], Dict[str, str]]:
        nlp = spacy.load("en_core_web_sm")
        matcher = PhraseMatcher(nlp.vocab)
        implicative_pairs = [item.split(":") for item in wordlist] #seperate predicates and inferences
        implicative_predicates = [pair[0] for pair in implicative_pairs]
        implicative_inferences_dict = {pair[0].split()[0]:pair[1] for pair in implicative_pairs} #dictionary mapping predicates to inferences
        implicative_verbs = set([p.split()[0] for p in implicative_predicates])

        # add implicative predicates to matcher
        patterns = [nlp.make_doc(text) for text in implicative_predicates]
        matcher.add("IMPL_PRED_LIST", None, *patterns)
        return (matcher, implicative_verbs, implicative_inferences_dict)


if __name__ == '__main__':
    implicative_extractor = ImplicativeExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        implicative_extractor.get_trigger_canonical_example(),
    ]

    for e in example_sentences:
        print(implicative_extractor.generate_presupposition(nlp(e)))

