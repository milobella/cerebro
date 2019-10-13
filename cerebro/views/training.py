import logging

from sanic import response
from sanic.exceptions import ServiceUnavailable
from sanic.request import Request
from sanic.views import HTTPMethodView

from cerebro.spacy.spacy_manager import SpaCyModelManager, ModelIsUpdatingException


class TrainingView(HTTPMethodView):

    def __init__(self, spacy_manager: SpaCyModelManager):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._spacy_manager = spacy_manager

    async def get(self, _: Request):
        if self._spacy_manager.is_updating:
            raise ServiceUnavailable()

        return response.text("The model should work properly", status=200)

    async def post(self, _: Request, model_id: str):
        self._logger.debug(f"Training model : {model_id}.")
        try:
            self._spacy_manager.update_model(model_id)
        except ModelIsUpdatingException as e:
            raise ServiceUnavailable(e)

        return response.text("Successfully triggered a training run.", status=202)


