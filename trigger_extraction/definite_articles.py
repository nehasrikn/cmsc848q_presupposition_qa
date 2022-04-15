import spacy
from typing import List, Optional, Dict, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class DefiniteArticleExtractor(PresuppositionExtractor):
    """
    Definite article (the): I saw the cat » There exists some contextually salient, unique cat.
    """

    @staticmethod
    def get_trigger_name() -> str:
        return 'definite_article'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "when is the year of the cat in chinese zodiac"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence.
        """
        triggers = []

        for token in sentence:
            if token.dep_ == 'det' and str(token).lower() == 'the':

                triggers.append({
                    'determiner': str(token),
                    'phrase': " ".join(map(str, [str(t) for t in token.head.subtree if t != token and t.dep_ not in ('punct')]))
                })

        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        return '[phrase] exists'

    @staticmethod
    def _presupposition_template_arguments(determiner: str, phrase: str) -> str:
        return [f'{phrase} exists', f'{phrase} is contextually unique']

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(DefiniteArticleExtractor._presupposition_template_arguments(**d))

        return presuppositions


if __name__ == '__main__':
    definite_article_extractor = DefiniteArticleExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        definite_article_extractor.get_trigger_canonical_example(),
        "which is the nearest country north of egypt",
        "who sings the best version of we wish you a merry christmas",
        "what are the four countries with a higher spanish-speaking population than the USA"

    ]

    for e in example_sentences:
        print(definite_article_extractor.generate_presupposition(nlp(e)))

