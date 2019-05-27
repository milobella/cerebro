import logging
from typing import Dict

from cerebro.model.nlp_repository import Repository
from cerebro.model.spacy_manager import SpacyManager
from cerebro.processing.data import NLPModel


class NotAvailableException(Exception):
    pass


def if_available(func):
    """Raise an exception if class is not available"""

    def wrapper(*args, **kwargs):
        if not args[0].is_available():
            raise NotAvailableException()
        return func(*args, **kwargs)

    return wrapper


def lock_it(func):
    """Lock the method call using the _is_available boolean attribute"""

    # noinspection PyProtectedMember
    def wrapper(*args, **kwargs):
        args[0]._is_available = False
        result = func(*args, **kwargs)
        args[0]._is_available = True
        return result

    return wrapper


class NLPManager:
    """
    The nlp manager ensures, in the following priority order, the synchronization between:
    - the database (which contains only the user defined nlp & ner);
    - the spacy folder (which contains the spacy default model + the user defined nlp & ner)
    - the "In memory" data (which contains the same data as spacy folder but accessible by understand function)

    It gives also the ability to make an understanding action on raw text (see understand method).

    If something goes wrong during the update, a rollback is done to the previous spacy folder.

    Since the update action could take a long time, all will be done asynchronously and
    """

    def __init__(self, repository: Repository, spacy_manager: SpacyManager):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._repository = repository
        self._spacy_manager = spacy_manager

        self._in_memory_data = None
        self._is_available = True

    def is_available(self):
        return self._is_available

    @if_available
    def get(self) -> NLPModel:
        """
        Get the user defined samples.
        Raise a NotAvailableException if busy.
        :return: model.
        """
        return self._repository.read()

    @if_available
    def understand(self, text) -> Dict:
        """
        Performs nlp & ner on a raw text.
        Raise a NotAvailableException if busy.
        :param text: raw text
        :return: nlp & ner result.
        """
        return self._spacy_manager.understand(text)

    @if_available
    @lock_it
    def load_data(self) -> None:
        """
        Only synchronize the model. Designed to be run at start.
        Still, raise a NotAvailableException if busy.
        """
        model = self._repository.read()
        self._spacy_manager.load_and_train(model)

    @if_available
    @lock_it
    def update(self, model: NLPModel) -> None:
        """
        Update and synchronize the model.
        Raise a NotAvailableException if busy.
        :param model: the model you want to import.
        """
        self._repository.update(model)
        model = self._repository.read()
        self._spacy_manager.load_and_train(model)
