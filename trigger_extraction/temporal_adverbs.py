import spacy
from typing import List, Dict, Optional, Tuple
from base_presupposition_extractor import PresuppositionExtractor


class TemporalAdverbExtractor(PresuppositionExtractor):
    """
    Adverbial embedded clauses headed by prepositions such as "before", "after", "since", 
    and "while" presuppose the content of the clause they embed. The sentence "Lisa petted
    Tom's cat after she washed her hands" presupposes that "Lisa washed her hands". 
    Extracted sentences contain adverbial clauses headed by "after", "since", "before",
    "because", and "while".
    """

    TEMPORAL_PREPOSITIONS = ['before', 'after', 'while', 'since', 'because']
    ACCEPTED_HEAD_TAGS = {
        'VBG': 'gerund',
        'VBN': 'past-participle',
        'VBD': 'past',
        'VBP': 'non-3sg-present',
        'VBZ': '3sg-present',
        'VB': 'base',
    }

    @staticmethod
    def get_trigger_name() -> str:
        return 'temporal_adverb'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "He took them to the NL Championship Series last year before being swept by the Atlanta Braves."

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        """
        Returns whether or not trigger is found in sentence, and 
        preposition and embedded clause head tag if found.
        """

        triggers = []

        words = [t.text for t in sentence]
        preps_in_sentence = [word for word in sentence if word.lemma_ in TemporalAdverbExtractor.TEMPORAL_PREPOSITIONS]
        if len(preps_in_sentence) > 0:
            for prep in preps_in_sentence:
                prep_children = [child for child in prep.children]
                prep_tags = [child.tag_ for child in prep_children] # get the tag(s) of the immediate child
                # check if tag is accepted (must be a verbal category)
                accepted_prep_tags = list(set(prep_tags) & set(TemporalAdverbExtractor.ACCEPTED_HEAD_TAGS.keys()))
                if len(prep_children) > 0 and len(accepted_prep_tags) > 0:
                    triggers.append({
                        'temporal_preposition': prep.text,
                        'tags': prep_tags
                    })

        return (True, triggers) if triggers else (False, [])

    @staticmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    def _presupposition_template_arguments(temporal_preposition: str, tags: List[str]) -> str:
        return f'{temporal_preposition}'

    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []

        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(TemporalAdverbExtractor._presupposition_template_arguments(**d))

        return presuppositions


if __name__ == '__main__':
    temporal_adverb_extractor = TemporalAdverbExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = [
        temporal_adverb_extractor.get_trigger_canonical_example(),
    ]

    for e in example_sentences:
        print(temporal_adverb_extractor.generate_presupposition(nlp(e)))

