import spacy
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod


class PresuppositionExtractor(ABC):
    
    @staticmethod
    @abstractmethod
    def get_trigger_name() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_trigger_canonical_example() -> str:
        raise NotImplementedError

    @abstractmethod
    def find_trigger(sentence: spacy.tokens.doc.Doc) -> Tuple[bool, Optional[List[str]]]:
        """
        Returns whether or not trigger is found in sentence and the token(s) that caused
        the method to fire.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def presupposition_template() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_presupposition(sentence: str) -> str:
        raise NotImplementedError

    @staticmethod
    def get_wordlist(wordlist_path: str) -> Optional[List[str]]:
        return None

    