#!/usr/bin/env python
# coding: utf8
import configparser
import logging
from threading import Thread

from sanic import Sanic

from cerebro.model.nlp_repository_fake import NLPRepositoryFake
from cerebro.model.spacy_manager import SpacyManager
from cerebro.processing.nlp_manager import NLPManager
from cerebro.views.understanding import UnderstandingView
from cerebro.views.web import HtmlView
from cerebro.utils import config_to_dict

# Initialize logger
logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)
logger = logging.getLogger()

# Initialize the config
logger.debug("Initialize configuration ...")
_config = configparser.ConfigParser()
_config.read('cerebro.ini')
logger.debug("Successfully initialized configuration ! {0}".format(config_to_dict(_config)))

# Initialize the sanic app
_app = Sanic()


def run(host: str = None, port: int = None):
    # Initialize parameters (host and port parameters can be overriden by command line)
    host = _config['server'].get('url') if host is None else host
    port = _config['server'].getint('port') if port is None else port
    spacy_manager_options = {
        "min_score": _config["spacy"].getfloat("min_score", fallback=None),
        "model": _config["spacy"].get("model", fallback=None),
        "iterations": _config["spacy"].getint("iterations", fallback=None)
    }
    # Ensure that default values of spacy manager ctor will be used
    spacy_manager_options = {key: value for key, value in spacy_manager_options.items() if value is not None}

    # Build the project's architecture
    repository = NLPRepositoryFake()
    spacy_manager = SpacyManager(**spacy_manager_options)
    manager = NLPManager(repository, spacy_manager)

    # Server routing
    _app.add_route(HtmlView.as_view(), '/')
    _app.add_route(UnderstandingView.as_view(manager), '/understand')

    # Asynchronous call to data loading
    Thread(target=manager.load_data).start()

    # Run the server
    _app.run(
        host=host,
        port=port,
    )
