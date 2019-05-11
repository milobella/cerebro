#!/usr/bin/env python
# coding: utf8

import configparser

import spacy
from sanic import response, Sanic
from sanic.response import json

import logging
 
from logging.handlers import RotatingFileHandler
 
# Initialize logger (TODO: industrialize it)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# Initialize the config
logger.debug("Initialize configuration ...")
_config = configparser.ConfigParser()
_config.read('cerebro.ini')
logger.debug("Successfully initialized configuration ! {0}".format(_config))
_min_score = _config["nlp"].getfloat("min_score")

# Initialize the sanic app
_app = Sanic()

# Load the spacy model
logger.debug("Loading Spacy Data ...")
_nlp = spacy.load("data")
logger.debug("Successfully loaded Spacy Data !")


def main():
    # Run the app
    _app.run(
        host=_config['server']['url'],
        port=_config['server'].getint('port')
    )


@_app.route('/')
async def home(request):
    return response.html('<p>Hello world!</p>')


@_app.route('/understand', methods=["GET", "POST"],)
async def understand(request):
    """
    Understand handler : client give a text query and we return a simplified version of the spaCy result document.
    :param request: user's request, contains the text query
    :return: simple json object with intents and entities.
        - intents: list of intents with its label and score, sorted by decreasing score;
        - entities: list of entities with its label and text (literal value).
    """

    # Build the recognition document from text dictated by user.
    _text = request.args["query"][0] if "GET" == request.method else request.json["text"]
    _doc = _nlp(_text)

    # Get entities from document (using trained NER - Named Entity Recognition).
    entities = [{"label": ent.label_, "text": ent.text} for ent in _doc.ents]

    # Get intents from document (using trained text categories). We sort it by decreasing score
    intents = [{"label": name, "score": score} for name, score in _doc.cats.items() if score > _min_score]
    intents = sorted(intents, key=lambda intent: intent['score'], reverse=True)

    # Returns what spaCy understood in a simplified format
    return json({
        "intents": intents,
        "entities": entities
    })


if __name__ == '__main__':
    main()
