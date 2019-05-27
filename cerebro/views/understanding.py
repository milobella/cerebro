import warnings

from sanic.exceptions import ServerError
from sanic.response import json
from sanic.views import HTTPMethodView

from cerebro.processing.nlp_manager import NLPManager, NotAvailableException


class UnderstandingView(HTTPMethodView):

    def __init__(self, nlp_manager: NLPManager):
        self._nlp_manager = nlp_manager

    async def get(self, request):
        warnings.warn(
            "Shouldn't use this endpoint anymore! Now use POST with text in body.",
            DeprecationWarning
        )
        return self._understand(request.args["query"][0])

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
        try:
            return json(self._nlp_manager.understand(text))
        except NotAvailableException:
            raise ServerError("Service unavailable.", status_code=503)
