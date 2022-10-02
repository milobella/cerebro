import pytest
import requests
import json
from grappa import should


class RestApi:
    def __init__(self, url: str):
        self._url = url

    def hello_world(self):
        return requests.get(f"{self._url}/")

    def understand(self, text: str):
        return requests.post(f"{self._url}/understand", json.dumps({"text": text}))


# noinspection PyStatementEffect
@pytest.mark.integration
class TestRestApiDeprecated(object):

    @classmethod
    def setup_class(cls):
        cls._api = RestApi("http://localhost:9444")

    def test_hello_world(self):
        resp = self._api.hello_world()
        resp.ok | should.be.true

    def test_understand__hello(self):
        resp = self._api.understand("bonjour")
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
        result["entities"][0] | should.be.equal.to({'label': 'SHOPITEM', 'text': 'fraises'})

    def test_understand__trigger_shopping_list(self):
        resp = self._api.understand("on fait la liste de course")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["intents"][0]['label'] | should.be.equal.to('TRIGGER_SHOPPING_LIST')
        result["entities"] | should.be.empty
