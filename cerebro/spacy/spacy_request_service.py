import logging
from typing import Dict

from cerebro.spacy.spacy_manager import SpaCyModelManager


class SpaCyRequestService:
    def __init__(self, spacy_manager: SpaCyModelManager, min_score: float):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._min_score = min_score
        self._spacy_manager = spacy_manager

    def understand(self, text: str) -> Dict:
        # Build the recognition document from text dictated by user.
        _doc = self._spacy_manager.model(text)

        # Get entities from document (using trained NER - Named Entity Recognition).
        entities = [{"label": ent.label_, "text": ent.text} for ent in _doc.ents]

        # Get intents from document (using trained text categories). We sort it by decreasing score
        intents = [{"label": name, "score": score} for name, score in _doc.cats.items() if score > self._min_score]
        intents = sorted(intents, key=lambda intent: intent['score'], reverse=True)

        # Get lemmas from document
        lemmas = [token.lemma_ for token in _doc]

        # Get verbs from document
        verbs = [token.lemma_ for token in _doc if token.pos_ == "VERB"]

        # Get a simplified version of tokens
        tokens = [self._simplify(token) for token in _doc]

        # Returns what spaCy understood in a simplified format
        return {
            "intents": intents,
            "entities": entities,
            "verbs": verbs,
            "lemmas": lemmas,
            "tokens": tokens
        }

    @staticmethod
    def _simplify(token):
        return {
            "lemma": token.lemma_,
            "tag": token.tag_,
            "pos": token.pos_,
            "literal": token.text,
            "head_index": token.head.i
        }
