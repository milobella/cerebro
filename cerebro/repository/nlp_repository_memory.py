from typing import List, Dict

from cerebro.repository.nlp_repository import Repository


class NLPRepositoryMemory(Repository):
    def __init__(self):
        self._samples = {}
        self._categories = {}
        self._entities = {}

    def get_samples(self, model_id: str, start: int, limit: int) -> List[Dict]:
        return self._samples[model_id][start: start + limit]

    def get_categories(self, model_id: str) -> List[str]:
        return self._categories[model_id]

    def get_entities(self, model_id: str) -> List[str]:
        return self._entities[model_id]

    def update(self, model_id: str, samples: List[Dict]):
        categories = set([])
        [categories.update(sample["categories"]) for sample in samples]
        self._categories[model_id] = categories

        entities = set([])
        [entities.update([ent["name"] for ent in sample["entities"]]) for sample in samples if "entities" in sample]
        self._entities[model_id] = entities
        self._samples[model_id] = samples

    def clear(self, model_id: str):
        del self._categories[model_id]
        del self._entities[model_id]
        del self._samples[model_id]
