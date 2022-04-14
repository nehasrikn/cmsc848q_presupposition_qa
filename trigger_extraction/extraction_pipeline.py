import spacy
from typing import List, Optional, Tuple, Dict

from base_presupposition_extractor import PresuppositionExtractor
from change_of_state import ChangeOfStateExtractor
from comparatives import ComparativeExtractor
from continuation_of_state import ContinuationOfStateExtractor
from embedded_questions import EmbeddedQuestionExtractor
from factives import FactiveExtractor
from implicatives import ImplicativeExtractor
from numeric_determiners import NumericDeterminerExtractor
from re_verbs import RePrefixedVerbExtractor
from temporal_adverbs import TemporalAdverbExtractor

class PresuppositionExtractionPipeline:

	def __init__(self, extractors: List[PresuppositionExtractor]) -> None:

		self.extractors = extractors

	def run(self, sentence: spacy.tokens.doc.Doc) -> Dict[str,  Tuple[bool, Optional[List[str]]]]:
		return {
			e.get_trigger_name(): e().find_trigger(nlp(sentence)) 
			for e in self.extractors
		}

	def get_components(self) -> List[str]:
		return [e.get_trigger_name() for e in self.extractors]

if __name__ == '__main__':

	nlp = spacy.load("en_core_web_sm")

	sentence = "He cried before he danced."

	extractors = [
		ChangeOfStateExtractor, 
		ComparativeExtractor, 
		ContinuationOfStateExtractor,
		EmbeddedQuestionExtractor,
		FactiveExtractor,
		ImplicativeExtractor,
		NumericDeterminerExtractor,
		RePrefixedVerbExtractor,
		TemporalAdverbExtractor
	]

	pipeline = PresuppositionExtractionPipeline(extractors=extractors)

	print(pipeline.run(nlp(sentence)))

	