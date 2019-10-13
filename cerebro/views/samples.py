import logging

import fastjsonschema as fastjsonschema
from bson.json_util import dumps
from fastjsonschema import JsonSchemaException
from sanic import response
from sanic.exceptions import InvalidUsage
from sanic.request import Request
from sanic.views import HTTPMethodView

from cerebro.repository.nlp_repository import Repository


class SamplesView(HTTPMethodView):
    def __init__(self, nlp_repository: Repository):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._nlp_repository = nlp_repository
        self._validator = fastjsonschema.compile({
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "categories": {"type": "array", "items": {"type": "string"}},
                    "entities": {"type": "array", "items": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "number"},
                            "end": {"type": "number"},
                            "name": {"type": "string"},
                        },
                        "required": ["start", "end", "name"]
                    }}
                },
                "required": ["text", "categories"]
            }
        })

    async def get(self, request: Request, model_id: str):
        limit = int(request.args.get("limit", '10'))
        start = int(request.args.get("start", '0'))
        samples = self._nlp_repository.get_samples(model_id, start, limit)
        return response.json({
            "results": samples,
            "limit": limit,
            "size": len(samples),
            "start": start
        }, dumps=dumps)

    async def put(self, request: Request, model_id: str):
        samples = request.json
        try:
            self._validator(samples)
        except JsonSchemaException as e:
            raise InvalidUsage(e)
        self._logger.debug(f"Uploading {len(samples)} samples.")
        self._nlp_repository.update(model_id, samples)
        return response.text(f"Successfully updated the model {model_id}.", status=204)

    async def delete(self, request: Request, model_id: str):
        self._nlp_repository.clear(model_id)
        return response.json({})
