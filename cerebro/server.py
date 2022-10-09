#!/usr/bin/env python
# coding: utf8
import logging
from typing import Dict, Any

import yaml as yaml
from sanic import Sanic
from sanic.config import Config

from cerebro.repository.nlp_repository_memory import NLPRepositoryMemory
from cerebro.repository.nlp_repository_mongo import NLPRepositoryMongo
from cerebro.spacy.spacy_manager import SpaCyModelManager
from cerebro.spacy.spacy_request_service import SpaCyRequestService
from cerebro.views.samples import SamplesView
from cerebro.views.training import TrainingView
from cerebro.views.understanding import UnderstandingView
from cerebro.views.web import HtmlView


class YamlConfig(Config):
    def __init__(self, *args, path: str, **kwargs):
        super().__init__(*args, **kwargs)

        with open(path, "r") as f:
            self.apply(yaml.safe_load(f))

    def apply(self, config):
        self.update(self._to_uppercase(config))

    def _to_uppercase(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        retval: Dict[str, Any] = {}
        for key, value in obj.items():
            upper_key = key.upper()
            if isinstance(value, list):
                retval[upper_key] = [
                    self._to_uppercase(item) for item in value
                ]
            elif isinstance(value, dict):
                retval[upper_key] = self._to_uppercase(value)
            else:
                retval[upper_key] = value
        return retval


# Initialize logger
logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)
logger = logging.getLogger()

# Initialize the sanic app
config = YamlConfig(path="cerebro.yaml")
app = Sanic(name="cerebro", config=config)

if config["CEREBRO"]["FEATURES"]["USE_MONGO"]:
    repository = NLPRepositoryMongo(
        url=config["CEREBRO"]["MONGODB"]["URL"],
        database=config["CEREBRO"]["MONGODB"]["DATABASE"]
    )
else:
    repository = NLPRepositoryMemory()

app.add_route(HtmlView.as_view(), '/')
app.add_route(SamplesView.as_view(repository), '/models/<model_id:str>/samples')

if config["CEREBRO"]["FEATURES"]["USE_SPACY"]:
    spacy_manager = SpaCyModelManager(
        repository, model=config["CEREBRO"]["SPACY"]["MODEL"],
        iterations=config["CEREBRO"]["SPACY"]["ITERATIONS"],
        chunk_size=config["CEREBRO"]["SPACY"]["CHUNK_SIZE"]
    )
    spacy_request = SpaCyRequestService(
        spacy_manager, min_score=config["CEREBRO"]["SPACY"]["MIN_SCORE"]
    )

    app.add_route(UnderstandingView.as_view(spacy_request), '/understand')
    app.add_route(TrainingView.as_view(spacy_manager), '/models/<model_id:str>/train')

    # # Asynchronous call to SpaCy training
    # spacy_manager.update_model("default")
else:
    logger.warn(
        "\n#######  !! SpaCy has been disabled !!  ########"
        "\n Cerebro is not really interesting without SpaCy ;)."
        "\n You can reactivate it with this line in config:"
        "\n ================="
        "\n\t[features]"
        "\n\tuse_spacy = true"
        "\n ================="
        "\n################################################")

if __name__ == "__main__":
    app.run()
