#!/usr/bin/env python
# coding: utf8

import configparser

import spacy
from sanic import response, Sanic
from sanic.response import json

# Initialize the config
_config = configparser.ConfigParser()
_config.read('cerebro.ini')

# Initialize the sanic app
_app = Sanic()

# Load the spacy model
_nlp = spacy.load("data")


def main():
    # Run the vibora app
    _app.run(
        host=_config['server']['url'],
        port=_config['server'].getint('port')
    )


@_app.route('/')
async def home(request):
    return response.html('<p>Hello world!</p>')


@_app.route('/understand')
async def understand(request):
    result = []
    confidences = _nlp(request.args["query"][0]).cats
    for intent, confidence in confidences.items():
        if confidence > 0.1:
            # TODO: find a way to get parameters dynamically
            result.append({
                "intent": intent,
                "score": confidence,
                "parameters": {} if intent != "ADD_TO_LIST" else {"items": ["des tomates", "des courgettes"]}
            })
    return json(result)


if __name__ == '__main__':
    main()
