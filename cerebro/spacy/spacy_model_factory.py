import logging
import random
from typing import List, Dict

import spacy
from spacy.util import compounding, minibatch


class SpacyModelFactory:
    def __init__(self, model: str, iterations: int, categories: List[str], entities: List[str]):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._nlp = None
        self._categories = categories
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
        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if 'ner' not in self._nlp.pipe_names:
            ner = self._nlp.create_pipe('ner')
            self._nlp.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = self._nlp.get_pipe('ner')

        for entity in self._entities:
            ner.add_label(entity)

        # === Load categories ===
        # add the text classifier to the pipeline if it doesn't exist
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if 'textcat' not in self._nlp.pipe_names:
            textcat = self._nlp.create_pipe('textcat')
            self._nlp.add_pipe(textcat, last=True)
        # otherwise, get it, so we can add labels to it
        else:
            textcat = self._nlp.get_pipe('textcat')

        for cat in self._categories:
            textcat.add_label(cat)

    def register_samples(self, samples: List[Dict]):
        # Build the train data
        train_categories_data = []
        train_entities_data = []
        for sample in samples:
            # Append the train data for category
            train_categories_data.append((
                sample["text"],
                {'cats': {cat: 1. if cat in sample["categories"] else 0. for cat in self._categories}}
            ))

            # Append the train data for entities
            if "entities" in sample and len(sample["entities"]) != 0:
                train_entities_data.append((
                    sample["text"],
                    {'entities': [(ent["start"], ent["end"], ent["name"]) for ent in sample["entities"]]}
                ))

        # Perform the trains
        self._logger.debug(f"Training {len(samples)} samples on SpaCy Data Model : {self._model}... Could take time.")
        self._train_categories(train_categories_data)
        self._train_ner(train_entities_data)
        self._logger.debug("Successfully trained SpaCy Data !")

    def _train_ner(self, train_entities_data):

        # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in self._nlp.pipe_names if pipe != 'ner']
        with self._nlp.disable_pipes(*other_pipes):  # only train NER
            optimizer = self._nlp.begin_training()
            losses = {}
            for itn in range(self._iterations):
                random.shuffle(train_entities_data)

                # batch up the examples using spaCy's minibatch
                batches = minibatch(train_entities_data, size=compounding(4., 32., 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self._nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        sgd=optimizer,  # callable to update weights
                        losses=losses)
            self._logger.debug('Losses ', losses)

    def _train_categories(self, train_categories_data):

        # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in self._nlp.pipe_names if pipe != 'textcat']
        with self._nlp.disable_pipes(*other_pipes):  # only train textcat
            optimizer = self._nlp.begin_training()
            # print("Training the model...")
            # print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))

            for itn in range(self._iterations):
                losses = {}
                batches = minibatch(train_categories_data, size=compounding(4., 32., 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self._nlp.update(texts, annotations, sgd=optimizer, losses=losses)

                # with textcat.model.use_params(optimizer.averages):
                #     # evaluate on the dev data split off in load_data()
                #     scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
                # print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
                #       .format(losses['textcat'], scores['textcat_p'],
                #               scores['textcat_r'], scores['textcat_f']))
