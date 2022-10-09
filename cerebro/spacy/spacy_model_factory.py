import logging
import random
from typing import List, Dict

import spacy
from spacy.training import Example
from spacy.util import compounding, minibatch

PIPE_INTENT = "textcat"
PIPE_ENTITY = "ner"


class SpacyModelFactory:
    def __init__(self, model: str, iterations: int, intents: List[str], entities: List[str]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._nlp = None
        self._intents = intents
        self._entities = entities

        self._model = model
        self._iterations = iterations

    def get_nlp(self):
        return self._nlp

    def load_model(self):
        """
        We start the creation of a new nlp.
        :return:
        """
        self._logger.debug(f"Loading Spacy Data Model : {self._model}... Could take time.")
        self._nlp = spacy.load(self._model)
        self._logger.debug("Successfully loaded Spacy Data !")

        # === Load entities ===
        if PIPE_ENTITY not in self._nlp.pipe_names:
            self._nlp.add_pipe(PIPE_ENTITY, last=True)

        entity_pipe = self._nlp.get_pipe(PIPE_ENTITY)
        for entity in self._entities:
            entity_pipe.add_label(entity)

        # === Load categories ===
        if PIPE_INTENT not in self._nlp.pipe_names:
            self._nlp.add_pipe(PIPE_INTENT, last=True)

        intent_pipe = self._nlp.get_pipe(PIPE_INTENT)
        for intent in self._intents:
            intent_pipe.add_label(intent)

    def register_samples(self, samples: List[Dict]):
        # Build the train data
        train_intent_data = []
        train_entity_data = []
        for sample in samples:
            # Append the train data for category
            train_intent_data.append((
                sample["text"],
                {'cats': {cat: 1. if cat in sample["categories"] else 0. for cat in self._intents}}
            ))

            # Append the train data for entities
            if "entities" in sample and len(sample["entities"]) != 0:
                train_entity_data.append((
                    sample["text"],
                    {'entities': [(ent["start"], ent["end"], ent["name"]) for ent in sample["entities"]]}
                ))

        # Perform the trains
        self._logger.debug(f"Training {len(samples)} samples on SpaCy Data Model : {self._model}... Could take time.")
        self._train(PIPE_INTENT, train_intent_data)
        self._train(PIPE_ENTITY, train_entity_data)
        self._logger.debug("Successfully trained SpaCy Data !")

    def _train(self, pipe_name: str, train_data):
        with self._nlp.select_pipes(enable=[pipe_name]):  # only train given pipe
            examples = []
            for text, annots in train_data:
                examples.append(Example.from_dict(self._nlp.make_doc(text), annots))
            self._nlp.initialize(lambda: examples)
            losses = {}
            for itn in range(self._iterations):
                random.shuffle(examples)

                # batch up the examples using spaCy's minibatch
                for batch in minibatch(examples, size=compounding(4., 32., 1.001)):
                    self._nlp.update(batch, losses=losses)
            self._logger.debug('Losses ', losses)
