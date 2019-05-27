import logging
import random
from typing import Dict

import spacy
from spacy.util import compounding, minibatch

from cerebro.processing.data import NLPModel


class SpacyManager:
    def __init__(self, min_score: float = 0.1, model: str = "fr_core_news_md", iterations: int = 40):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._min_score = min_score
        self._model = model
        self._iterations = iterations

        self._nlp = None

    def load_and_train(self, model: NLPModel):
        # Performs the load
        self._logger.debug(f"Loading Spacy Data Model : {self._model}... Could take time.")
        self._nlp = spacy.load(self._model)
        self._logger.debug("Successfully loaded Spacy Data !")

        # Post process on categories
        all_categories = model.get_all_categories()
        for sample in model:
            for cat in all_categories:
                if cat not in sample.categories:
                    sample.add_zero_category(cat)

        # Post process on entities
        all_entities = model.get_all_entities()

        # Build the train data
        train_categories_data = []
        train_entities_data = []
        for sample in model:
            train_categories_data.append(sample.get_categories_train())
            if len(sample.entities) != 0:
                train_entities_data.append(sample.get_entities_train())

        # Perform the trains
        self._logger.debug(f"Training Spacy Data Model : {self._model}... Could take time.")
        self._train_categories(all_categories, train_categories_data)
        self._train_ner(all_entities, train_entities_data)
        self._logger.debug("Successfully trained Spacy Data !")

    def understand(self, text: str) -> Dict:
        # Build the recognition document from text dictated by user.
        _doc = self._nlp(text)

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

    def _train_ner(self, all_entities, train_entities_data):
        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if 'ner' not in self._nlp.pipe_names:
            ner = self._nlp.create_pipe('ner')
            self._nlp.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = self._nlp.get_pipe('ner')

        for entity in all_entities:
            ner.add_label(entity)

        # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in self._nlp.pipe_names if pipe != 'ner']
        with self._nlp.disable_pipes(*other_pipes):  # only train NER
            optimizer = self._nlp.begin_training()
            for itn in range(self._iterations):
                random.shuffle(train_entities_data)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(train_entities_data, size=compounding(4., 32., 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self._nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        sgd=optimizer,  # callable to update weights
                        losses=losses)
                print('Losses', losses)

    def _train_categories(self, all_categories, train_categories_data):
        # add the text classifier to the pipeline if it doesn't exist
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if 'textcat' not in self._nlp.pipe_names:
            textcat = self._nlp.create_pipe('textcat')
            self._nlp.add_pipe(textcat, last=True)
        # otherwise, get it, so we can add labels to it
        else:
            textcat = self._nlp.get_pipe('textcat')

        for cat in all_categories:
            textcat.add_label(cat)

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

    @staticmethod
    def _simplify(token):
        return {
            "lemma": token.lemma_,
            "tag": token.tag_,
            "pos": token.pos_,
            "literal": token.text,
            "head_index": token.head.i
        }
