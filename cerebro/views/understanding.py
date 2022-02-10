import logging
import warnings

from sanic.exceptions import ServiceUnavailable
from sanic.response import json
from sanic.views import HTTPMethodView

from cerebro.spacy.spacy_manager import ModelIsUpdatingException, ModelNeedAnUpdateException
from cerebro.spacy.spacy_request_service import SpaCyRequestService


class UnderstandingView(HTTPMethodView):

    def __init__(self, request_service: SpaCyRequestService):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._request_service = request_service

    async def post(self, request):
        return self._understand(request.json["text"])

    def _understand(self, text: str):
        """
        Understand handler : client give a text query and we return a simplified version of the spaCy result document.
        :param text: the text query
        :return: simple json object with intents and entities.
            - intents: list of intents with its label and score, sorted by decreasing score;
            - entities: list of entities with its label and text (literal value).
            - verbs: list of the verbs in the sentence.
            - lemmas: list of lemmas in the sentence.
            - list of the tokens in the sentence.
        """
        self._logger.debug(f"Trying to understand sentence : {text}")
        try:
            return json(self._request_service.understand(text))
        except (ModelIsUpdatingException, ModelNeedAnUpdateException) as e:
            raise ServiceUnavailable(e)
