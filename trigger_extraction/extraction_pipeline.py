import spacy
import pprint
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

class PresuppositionExtractionPipeline:

	def __init__(self, extractors: List[PresuppositionExtractor]) -> None:

		self.extractors = extractors

	def run(self, sentence: spacy.tokens.doc.Doc) -> Dict[str,  Tuple[bool, Optional[List[str]]]]:
		return {
			e.get_trigger_name(): (e().find_trigger_instances(nlp(sentence)), e().generate_presupposition(nlp(sentence)))
			for e in self.extractors
		}

	def get_components(self) -> List[str]:
		return [e.get_trigger_name() for e in self.extractors]

if __name__ == '__main__':

	nlp = spacy.load("en_core_web_sm")

	sentence = "which linguist invented grass"

	extractors = [
		ChangeOfStateExtractor, 
		ComparativeExtractor, 
		ContinuationOfStateExtractor,
		CounterfactualExtractor,
		DefiniteArticleExtractor,
		EmbeddedQuestionExtractor,
		FactiveExtractor,
		ImplicativeExtractor,
		NumericDeterminerExtractor,
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

	pipeline = PresuppositionExtractionPipeline(extractors=extractors)

	pp = pprint.PrettyPrinter(compact=True)
	print(sentence)
	pp.pprint(pipeline.run(nlp(sentence)))

	