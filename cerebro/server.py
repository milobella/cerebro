#!/usr/bin/env python
# coding: utf8
import logging

from sanic import Sanic

from cerebro.repository.nlp_repository import Repository
from cerebro.repository.nlp_repository_fake import NLPRepositoryFake
from cerebro.repository.nlp_repository_mongo import NLPRepositoryMongo
from cerebro.spacy.spacy_manager import SpaCyModelManager
from cerebro.spacy.spacy_request_service import SpaCyRequestService
from cerebro.views.samples import SamplesView
from cerebro.views.training import TrainingView
from cerebro.views.understanding import UnderstandingView
from cerebro.views.web import HtmlView


def run(**params):
    logger = logging.getLogger()

    # Initialize the sanic app
    _app = Sanic(name="cerebro", configure_logging=False)

    repository = build_repository(**params)

    _app.add_route(HtmlView.as_view(), '/')
    _app.add_route(SamplesView.as_view(repository), '/models/<model_id:string>/samples')

    if params["use_spacy"]:
        spacy_manager = SpaCyModelManager(
            repository, model=params["model"],
            iterations=params["iterations"],
            chunk_size=params["chunk_size"]
        )
        spacy_request = SpaCyRequestService(
            spacy_manager, min_score=params["min_score"]
        )

        _app.add_route(UnderstandingView.as_view(spacy_request), '/understand')
        _app.add_route(TrainingView.as_view(spacy_manager), '/models/<model_id>/train')

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

    # Run the server
    _app.run(
        host=params["host"],
        port=params["port"],
    )


def build_repository(**params) -> Repository:
    if params["use_mongo"]:
        return NLPRepositoryMongo(
            url=params["mongo_url"],
            database=params["mongo_database"]
        )
    else:
        return NLPRepositoryFake()
