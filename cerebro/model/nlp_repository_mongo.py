from cerebro.processing.data import NLPModel
from cerebro.model.nlp_repository import Repository


class NLPRepositoryMongo(Repository):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def read(self) -> NLPModel:
        pass

    def update(self, entity: NLPModel) -> bool:
        pass
