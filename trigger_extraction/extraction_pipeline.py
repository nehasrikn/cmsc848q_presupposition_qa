from change_of_state import ChangeOfStateExtractor
from comparatives import ComparativeExtractor
from continuation_of_state import ContinuationOfStateExtractor
from embedded_questions import EmbeddedQuestionExtractor
from factives import FactiveExtractor
from implicatives import ImplicativeExtractor
from numeric_determiners import NumericDeterminerExtractor
from re_verbs import RePrefixedVerbExtractor
from temporal_adverbs import TemporalAdverbExtractor

import spacy

if __name__ == '__main__':

	nlp = spacy.load("en_core_web_sm")

	sentence = "who is the current monarch of france"

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

	for e in extractors:
		if e().find_trigger(nlp(sentence))[0]:
			print(e.get_trigger_name())