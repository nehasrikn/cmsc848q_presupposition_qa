import spacy
from typing import List, Dict, Optional, Tuple
from base_presupposition_extractor import PresuppositionExtractor
from utils import get_dependents_string


class WhoQuestionExtractor(PresuppositionExtractor):
    """
    "Who did Jane talk to?" >> There is someone that Jane talked to.
    """
    
    @staticmethod
    def get_trigger_name() -> str:
        return 'who_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "who sings it's a hard knock life"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        triggers = []

        for token in sentence:
            if token.tag_.startswith('WP') and str(token).lower() == 'who':
                triggers.append({
                    'wh_word': str(token),
                    'verb_phrase': " ".join(map(str, [str(t) for t in token.head.subtree if t != token]))
                })

        return (True, triggers) if triggers else (False, [])


    @staticmethod
    def presupposition_template() -> str:
        return 'there is someone that [verb_phrase]'

    @staticmethod
    def _presupposition_template_arguments(wh_word: str, verb_phrase: str) -> str:
        return f'there is someone that {verb_phrase}'


    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []
        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(WhoQuestionExtractor._presupposition_template_arguments(**d))
        return presuppositions


class WhatQuestionExtractor(PresuppositionExtractor):
    """
    "what did the treaty of paris do for the US" >> there is something thatthe treaty of paris did for the US
    """
    
    @staticmethod
    def get_trigger_name() -> str:
        return 'what_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "what did the treaty of paris do for the US"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        triggers = []

        for token in sentence:
            if token.tag_.startswith('WP') and str(token).lower() == 'what':
                triggers.append({
                    'wh_word': str(token),
                    'verb_phrase': " ".join(map(str, [str(t) for t in token.head.subtree if t != token]))
                })

        return (True, triggers) if triggers else (False, [])


    @staticmethod
    def presupposition_template() -> str:
        return 'there is something that [verb_phrase]'

    @staticmethod
    def _presupposition_template_arguments(wh_word: str, verb_phrase: str) -> str:
        return f'there is something that {verb_phrase}'


    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []
        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(WhatQuestionExtractor._presupposition_template_arguments(**d))
        return presuppositions

class WhenQuestionExtractor(PresuppositionExtractor):
    """
    "what did the treaty of paris do for the US" >> there is something thatthe treaty of paris did for the US
    """
    
    @staticmethod
    def get_trigger_name() -> str:
        return 'when_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "when was the jury system abolished in india"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        triggers = []

        for token in sentence:
            if token.tag_ == 'WRB' and str(token).lower() == 'when':
                triggers.append({
                    'wh_word': str(token),
                    'phrase': " ".join(map(str, [str(t) for t in token.head.subtree if t != token]))
                })

        return (True, triggers) if triggers else (False, [])


    @staticmethod
    def presupposition_template() -> str:
        return 'there is some point in time that [phrase]'

    @staticmethod
    def _presupposition_template_arguments(wh_word: str, phrase: str) -> str:
        return f'there is some point in time that {phrase}'


    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []
        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(WhenQuestionExtractor._presupposition_template_arguments(**d))
        return presuppositions

class WhereQuestionExtractor(PresuppositionExtractor):
    """
    "what did the treaty of paris do for the US" >> there is something thatthe treaty of paris did for the US
    """
    
    @staticmethod
    def get_trigger_name() -> str:
        return 'where_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "where do harry potter’s aunt and uncle live"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        triggers = []

        for token in sentence:
            if token.tag_ == 'WRB' and str(token).lower() == 'where':
                triggers.append({
                    'wh_word': str(token),
                    'phrase': " ".join(map(str, [str(t) for t in token.head.subtree if t != token and t.dep_ != 'aux']))
                })

        return (True, triggers) if triggers else (False, [])


    @staticmethod
    def presupposition_template() -> str:
        return 'there is some place that that [phrase]'

    @staticmethod
    def _presupposition_template_arguments(wh_word: str, phrase: str) -> str:
        return f'there is some place that {phrase}'


    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []
        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(WhereQuestionExtractor._presupposition_template_arguments(**d))
        return presuppositions

class WhyQuestionExtractor(PresuppositionExtractor):
    """
    "what did the treaty of paris do for the US" >> there is something thatthe treaty of paris did for the US
    """
    
    @staticmethod
    def get_trigger_name() -> str:
        return 'why_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "why did jean valjean take care of cosette"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        triggers = []

        for token in sentence:
            if token.tag_ == 'WRB' and str(token).lower() == 'why':
                triggers.append({
                    'wh_word': str(token),
                    'phrase': " ".join(map(str, [str(t) for t in token.head.subtree if t != token and t.dep_ != 'aux']))
                })

        return (True, triggers) if triggers else (False, [])
        
    @staticmethod
    def presupposition_template() -> str:
        return 'there is some reason that [phrase]'

    @staticmethod
    def _presupposition_template_arguments(wh_word: str, phrase: str) -> str:
        return [f'{phrase}', f'there is some reason that {phrase}']


    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []
        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.extend(WhyQuestionExtractor._presupposition_template_arguments(**d))
        return presuppositions


class HowQuestionExtractor(PresuppositionExtractor):
    """
    "what did the treaty of paris do for the US" >> there is something thatthe treaty of paris did for the US
    """
    
    @staticmethod
    def get_trigger_name() -> str:
        return 'how_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "how did orchestra change in the romantic period"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        triggers = []

        for token in sentence:
            if token.tag_ == 'WRB' and str(token).lower() == 'how':
                triggers.append({
                    'wh_word': str(token),
                    'phrase': " ".join(map(str, [str(t) for t in token.head.subtree if t != token and t.dep_ != 'aux']))
                })

        return (True, triggers) if triggers else (False, [])
        
    @staticmethod
    def presupposition_template() -> str:
        return 'there is some way that [phrase]'

    @staticmethod
    def _presupposition_template_arguments(wh_word: str, phrase: str) -> str:
        return [f'{phrase}', f'there is some way that {phrase}']


    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []
        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.extend(HowQuestionExtractor._presupposition_template_arguments(**d))
        return presuppositions

class WhichQuestionExtractor(PresuppositionExtractor):
    """
    "what did the treaty of paris do for the US" >> there is something thatthe treaty of paris did for the US
    """
    
    @staticmethod
    def get_trigger_name() -> str:
        return 'which_question'

    @staticmethod
    def get_trigger_canonical_example() -> str:
        return "which philosopher advocated the idea of return to nature"

    def find_trigger_instances(self, sentence: spacy.tokens.doc.Doc) -> Tuple[bool, List[Dict[str, str]]]:
        triggers = []

        for token in sentence:
            if token.tag_ == 'WDT' and str(token).lower() == 'which':
                triggers.append({
                    'wh_word': str(token),
                    'phrase': " ".join(map(str, [str(t) for t in token.head.head.subtree if t != token]))
                })

        return (True, triggers) if triggers else (False, [])
        
    @staticmethod
    def presupposition_template() -> str:
        return 'some [phrase]'

    @staticmethod
    def _presupposition_template_arguments(wh_word: str, phrase: str) -> str:
        return f'some {phrase}'


    def generate_presupposition(self, sentence: spacy.tokens.doc.Doc) -> List[str]:
        presuppositions = []
        trigger_fired, trigger_instances = self.find_trigger_instances(sentence)
        if trigger_fired:
            for d in trigger_instances:
                presuppositions.append(WhichQuestionExtractor._presupposition_template_arguments(**d))
        return presuppositions


if __name__ == '__main__':
    who_question_extractor = WhoQuestionExtractor()
    what_question_extractor = WhatQuestionExtractor()
    when_question_extractor = WhenQuestionExtractor()
    where_question_extractor = WhereQuestionExtractor()
    why_question_extractor = WhyQuestionExtractor()
    how_question_extractor = HowQuestionExtractor()
    which_question_extractor = WhichQuestionExtractor()
    
    nlp = spacy.load("en_core_web_sm")

    example_sentences = {
        who_question_extractor: [
            who_question_extractor.get_trigger_canonical_example(),
            "who did the united states not have problems with on the high seas",
            "who played the agent in i can only imagine",
            "who played the ice cream man in this is us"
        ],
        what_question_extractor: [
            what_question_extractor.get_trigger_canonical_example(),
        ],
        when_question_extractor: [
            when_question_extractor.get_trigger_canonical_example(),
        ],
        where_question_extractor: [
            where_question_extractor.get_trigger_canonical_example(),
            "where does the term skin in the game come from",
            "where did the last name weaver come from",
            "where was hallmark movie a country wedding filmed"
        ],
        why_question_extractor: [
            why_question_extractor.get_trigger_canonical_example(),
            "why are there different time zones in australia",
            "where is the wailing wall and why is it a holy spot"
        ],
        how_question_extractor: [
            how_question_extractor.get_trigger_canonical_example(),
        ],
        which_question_extractor: [
            which_question_extractor.get_trigger_canonical_example(),
            "which locks are located on the north end of the panama canal",
            "which of these is japan’s worst environmental issue",
            "which among the following browsers have support to html5"
        ]
    }


    for extractor, examples in example_sentences.items():
        print('---', extractor.get_trigger_name(), '---')
        for e in examples:
            print(extractor.generate_presupposition(nlp(e)))

