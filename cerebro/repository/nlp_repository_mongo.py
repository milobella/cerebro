from typing import List, Set, Dict

from pymongo import MongoClient

from cerebro.repository.nlp_repository import Repository


class NLPRepositoryMongo(Repository):

    def __init__(self, url:str, database: str):
        self._url = url
        self._database = database

    @property
    def _client(self):
        return MongoClient(self._url)

    def get_samples(self, model_id: str, start: int, limit: int) -> List[Dict]:
        """
        Sample retrieve with pagination.
        :param model_id:
        :param start:
        :param limit:
        :return:
        """
        with self._client as client:
            db = client[self._database]
            return [doc for doc in db[f"samples_{model_id}"].find().skip(start).limit(limit)]

    def get_categories(self, model_id: str) -> List[str]:
        with self._client as client:
            return self._get_categories(client, model_id)

    def get_entities(self, model_id: str) -> List[str]:
        with self._client as client:
            return self._get_entities(client, model_id)

    def update(self, model_id: str, samples: List[Dict]):
        """
        The update is not really simple. For the moment, we rewrite categories and entities and make a classic
        insert of the samples.
        We use the same client in order to block any other connection at the same time.
        :param model_id:
        :param samples:
        :return:
        """
        with self._client as client:
            categories = set(self._get_categories(client, model_id))
            [categories.update(sample["categories"]) for sample in samples]
            self._update_categories(client, model_id, categories)

            entities = set(self._get_entities(client, model_id))
            [entities.update([ent["name"] for ent in sample["entities"]]) for sample in samples if "entities" in sample]
            self._update_entities(client, model_id, entities)

            self._update_samples(client, model_id, samples)

    def clear(self, model_id: str):
        with self._client as client:
            db = client[self._database]
            db.entities.delete_many({"model": model_id})
            db.categories.delete_many({"model": model_id})
            db[f"samples_{model_id}"].delete_many({})

    def _get_categories(self, client: MongoClient, model_id: str) -> List[str]:
        db = client[self._database]
        return [doc["name"] for doc in db.categories.find({"model": model_id})]

    def _get_entities(self, client: MongoClient, model_id: str) -> List[str]:
        db = client[self._database]
        return [doc["name"] for doc in db.entities.find({"model": model_id})]

    def _update_samples(self, client: MongoClient, model_id: str, samples: List[Dict]):
        db = client[self._database]
        db[f"samples_{model_id}"].delete_many({})
        db[f"samples_{model_id}"].insert_many(samples)

    def _update_categories(self, client: MongoClient, model_id: str, categories: Set[str]):
        """
        For sake of simplicity, we remove all categories of a model before to insert the new ones. Not so critical
        because there is not so many categories in a model.
        :param client:
        :param model_id:
        :param categories:
        :return:
        """
        db = client[self._database]
        db.categories.delete_many({"model": model_id})
        cat_objs = [{"name": cat, "model": model_id} for cat in categories]
        db.categories.insert_many(cat_objs)

    def _update_entities(self, client: MongoClient, model_id: str, entities: Set[str], ):
        """
        For sake of simplicity, we remove all entities of a model before to insert the new ones. Not so critical
        because there is not so many entities in a model.
        :param client:
        :param model_id:
        :param entities:
        :return:
        """
        db = client[self._database]
        db.entities.delete_many({"model": model_id})
        ent_objs = [{"name": ent, "model": model_id} for ent in entities]
        if len(ent_objs) >= 0:
            db.entities.insert_many(ent_objs)
