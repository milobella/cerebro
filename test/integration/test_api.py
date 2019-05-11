import pytest
import requests
import json
from grappa import should


class RestApi:
    def __init__(self, url: str):
        self._url = url

    def hello_world(self):
        return requests.get(f"{self._url}/")

    def understand_deprecated(self, text: str):
        return requests.get(f"{self._url}/understand?query={text}")

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

    def test_understand_deprecated__hello(self):
        resp = self._api.understand_deprecated("bonjour")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["entities"] | should.be.empty

    def test_understand_deprecated__time(self):
        resp = self._api.understand_deprecated("quelle heure il est")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["entities"] | should.be.empty

    def test_understand__hello(self):
        resp = self._api.understand("bonjour")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["entities"] | should.be.empty

    def test_understand__time(self):
        resp = self._api.understand("quelle heure il est")
        resp.ok | should.be.true
        result = json.loads(resp.content)
        result["intents"] | should.not_be.empty
        result["entities"] | should.be.empty
