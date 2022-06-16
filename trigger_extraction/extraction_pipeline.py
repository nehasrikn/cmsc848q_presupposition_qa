import spacy
import pprint
import argparse 
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict

from base_presupposition_extractor import PresuppositionExtractor
from change_of_state import ChangeOfStateExtractor
from comparatives import ComparativeExtractor
from continuation_of_state import ContinuationOfStateExtractor
from counterfactuals import CounterfactualExtractor
from definite_articles import DefiniteArticleExtractor
from embedded_questions import EmbeddedQuestionExtractor
from factives import FactiveExtractor
from implicatives import ImplicativeExtractor
from numeric_determiners import NumericDeterminerExtractor
from possessives import PossessiveExtractor
from re_verbs import RePrefixedVerbExtractor
from temporal_adverbs import TemporalAdverbExtractor
from wh_questions import (
    WhoQuestionExtractor, 
    WhatQuestionExtractor, 
    WhenQuestionExtractor, 
    WhereQuestionExtractor, 
    WhyQuestionExtractor, 
    HowQuestionExtractor, 
    WhichQuestionExtractor
)


EXTRACTORS = [
    ChangeOfStateExtractor, 
    ComparativeExtractor, 
    ContinuationOfStateExtractor,
    CounterfactualExtractor,
    DefiniteArticleExtractor,
    EmbeddedQuestionExtractor,
    FactiveExtractor,
    ImplicativeExtractor,
    NumericDeterminerExtractor,
    PossessiveExtractor,
    RePrefixedVerbExtractor,
    TemporalAdverbExtractor,
    WhoQuestionExtractor, 
    WhatQuestionExtractor, 
    WhenQuestionExtractor, 
    WhereQuestionExtractor, 
    WhyQuestionExtractor, 
    HowQuestionExtractor, 
    WhichQuestionExtractor
]

@dataclass
class Presupposition:
    """Represent an extracted presupposition"""
    sentence: str
    trigger_name: str
    metadata: Dict[str, str]
    template_presupposition: str
    annotated_presupposition: Optional[str]

    def __repr__(self):
      return self.template_presupposition

class PresuppositionExtractionResult:

    #TODO: Custom iter function

    def __init__(self, raw_presuppositions: Dict[str, Tuple[bool, ]]) -> None:
        self.raw_presuppositions = raw_presuppositions
        self.presuppositions = PresuppositionExtractionResult.parse_presup_dict(raw_presuppositions)
        self.fired_triggers = [k for k, v in self.raw_presuppositions.items( ) if v[0]]

    @staticmethod
    def parse_presup_dict(sentence: str, presup_dict: Dict[str, Tuple[bool, List[Dict[str, str]], str]]) -> List[Presupposition]:
        presuppositions = []
        for k, v in presup_dict.items():
            if v[0]: # trigger fired
                for i, p in enumerate(v[2]):
                    presuppositions.append(Presupposition(
                        sentence=sentence,
                        trigger_name=k,
                        metadata=p,
                        template_presupposition=v[2][i],
                        annotated_presupposition=None
                    )) 
        return presuppositions

    def __len__(self):
        return len(self.presuppositions)


class PresuppositionExtractionPipeline:

    def __init__(self, extractors: List[PresuppositionExtractor]) -> None:
        self.extractors = extractors

    def run(self, sentence: spacy.tokens.doc.Doc) -> Dict[str,  Tuple[bool, Optional[List[str]]]]:
        result =  {
            e.get_trigger_name(): (*e().find_trigger_instances(sentence), e().generate_presupposition(sentence))
            for e in self.extractors
        }
        return PresuppositionExtractionResult.parse_presup_dict(str(sentence), result)

    def get_components(self) -> List[str]:
        return [e.get_trigger_name() for e in self.extractors]

if __name__ == '__main__':
    """
    Usage: 
    python extraction_pipeline.py -s "When did the leaning tower of pisa start leaning?"
    """

    sentence = "which linguist invented grass"
    parser = argparse.ArgumentParser(description="Try out the presupposition extraction on a sentence")
    parser.add_argument('-s', '--sentence', dest='sent', type=str, help="Enter the sentence to be parsed", default=sentence)
    nlp = spacy.load("en_core_web_sm")

    pipeline = PresuppositionExtractionPipeline(extractors=EXTRACTORS)
    pp = pprint.PrettyPrinter(compact=True)
    
    args = parser.parse_args()
    sentence = args.sent 
    print(f"Sentence : {sentence}\n")
    
    presups = pipeline.run(nlp(sentence))
    print(presups)
    for presup in presups: 
        print(f"Trigger type: {presup.trigger_name}\tExtracted presup: {presup}")

    