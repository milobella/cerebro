import abc
from typing import List, Dict


class Repository(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_samples(self, model_id: str, start: int, limit: int) -> List[Dict]:
        raise NotImplementedError('users must define "get_samples" method to use this base class')

    @abc.abstractmethod
    def get_categories(self, model_id: str) -> List[str]:
        raise NotImplementedError('users must define "get_categories" method to use this base class')

    @abc.abstractmethod
    def get_entities(self, model_id: str) -> List[str]:
        raise NotImplementedError('users must define "get_entities" method to use this base class')

    @abc.abstractmethod
    def update(self, model_id: str, samples: List[Dict]):
        raise NotImplementedError('users must define "update" method to use this base class')

    @abc.abstractmethod
    def clear(self, model_id: str):
        raise NotImplementedError('users must define "clear" method to use this base class')
