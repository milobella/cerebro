import pytest
import requests
import json
from grappa import should


class Api:
    def __init__(self, url: str):
        self._url = url

    def hello_world(self):
        return requests.get(f"{self._url}/")

    def understand(self, text: str):
        return requests.post(f"{self._url}/understand", json.dumps({"text": text}))


# noinspection PyStatementEffect
@pytest.mark.integration
class TestApi(object):

    @classmethod
    def setup_class(cls):
        cls._api = Api("http://localhost:9444")

    def test_hello_world(self):
        resp = self._api.hello_world()
        resp.ok | should.be.true

    def test_understand__hello(self):
        resp = self._api.understand("BoNJoUr")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["intents"][0]['label'] | should.be.equal.to('HELLO')
        result["entities"] | should.be.empty

    def test_understand__time(self):
        resp = self._api.understand("quelle heure il est")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["intents"][0]['label'] | should.be.equal.to('GET_TIME')
        result["entities"] | should.be.empty

    def test_understand__shopping_list(self):
        resp = self._api.understand("ajoute des fraises à ma liste")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["intents"][0]['label'] | should.be.equal.to('ADD_TO_LIST')
        result["entities"] | should.not_be.empty
        result["entities"][0] | should.be.equal.to({'label': 'SHOPITEM', 'text': 'des fraises'})

    def test_understand__trigger_shopping_list(self):
        resp = self._api.understand("on fait la liste de course")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["intents"][0]['label'] | should.be.equal.to('TRIGGER_SHOPPING_LIST')
        result["entities"] | should.be.empty

    def test_understand__play_movie(self):
        resp = self._api.understand("je veux regarder the lego movie 2 dans la chambre")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["intents"][0]['label'] | should.be.equal.to('PLAY_MOVIE')
        result["entities"] | should.be.equal.to([
            {'label': 'title', 'text': 'the lego'},
            {'label': 'title', 'text': 'movie 2'},
            {'label': 'instrument', 'text': 'chambre'}
        ])
