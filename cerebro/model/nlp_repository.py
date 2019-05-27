import abc

from cerebro.processing.data import NLPModel


class Repository(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self) -> NLPModel:
        raise NotImplementedError('users must define "read" method to use this base class')

    @abc.abstractmethod
    def update(self, entity: NLPModel) -> bool:
        raise NotImplementedError('users must define "update" method to use this base class')
