import logging
from threading import Thread

from cerebro.repository.nlp_repository import Repository
from cerebro.spacy.spacy_model_factory import SpacyModelFactory


class ModelIsUpdatingException(Exception):
    pass


class ModelNeedAnUpdateException(Exception):
    pass


def if_not_updating(func):
    """Raise an exception if class is updating"""

    # noinspection PyProtectedMember
    def wrapper(*args, **kwargs):
        if args[0]._is_updating:
            raise ModelIsUpdatingException()
        return func(*args, **kwargs)

    return wrapper


class SpaCyModelManager:
    """
    This class is the container of the SpaCy model used by.
    It can neither update several models at the same time, nor use the model when it is updating.
    """

    def __init__(self, repository: Repository, model: str, iterations: int, chunk_size: int):
        """
        ctor
        :param repository: the repository where is stored the custom part of the model.
        :param model: the name of the base SpaCy model used.
        :param iterations: Number of iterations when trained.
        :param chunk_size: Max size of a chunk of samples.
        """

        self._logger = logging.getLogger(self.__class__.__name__)

        self._repository = repository
        self._model_source = model
        self._iterations = iterations
        self._chunk_size = chunk_size

        # The main model
        self._nlp_model = None

        self._is_updating = False

    @property
    def is_updating(self):
        return self._is_updating

    @property
    @if_not_updating
    def model(self):
        if self._nlp_model is None:
            raise ModelNeedAnUpdateException()
        return self._nlp_model

    @if_not_updating
    def update_model(self, model_id: str) -> None:
        """
        Synchronize the model from database to SpaCy data.
        Raise a NotAvailableException if busy.
        """
        # We lock the access to the data
        self._is_updating = True

        Thread(target=self._update_model, args=[model_id]).start()

    def _update_model(self, model_id: str) -> None:
        try:
            self._logger.info("Starting to create a new SpaCy repository.")
            categories = self._repository.get_categories(model_id)
            entities = self._repository.get_entities(model_id)
            nlp_factory = SpacyModelFactory(model=self._model_source, iterations=self._iterations,
                                            categories=categories, entities=entities)
            nlp_factory.load_model()
            start = 0
            while "Some samples are remaining":
                samples = self._repository.get_samples(model_id, start, self._chunk_size)
                nlp_factory.register_samples(samples)
                if len(samples) < self._chunk_size:
                    break
                start += self._chunk_size

            # If no exception occurred, we can update the nlp
            self._nlp_model = nlp_factory.get_nlp()

            self._logger.info("The SpaCy model has been successfully updated.")
        except Exception as e:
            self._logger.error("A problem occurred in the creation of SpaCy model. Action has been aborted.", e)
        finally:
            # Unlock anyway at the end of the thread
            self._is_updating = False
