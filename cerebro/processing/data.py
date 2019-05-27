from typing import List, Set


class NamedEntity:
    def __init__(self, start: int = 0, end: int = 0, value: str = ""):
        self.start = start
        self.end = end
        self.value = value

    def train_form(self):
        return self.start, self.end, self.value


class Category:
    def __init__(self, name: str = "", confidence: float = 1.):
        self.name = name
        self.confidence = confidence

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        else:
            return self.name == other.name


class Sample:
    def __init__(self, document: str = "", categories: List[Category] = None, entities: List[NamedEntity] = None):
        if categories is None:
            categories = []
        if entities is None:
            entities = []
        self.document = document
        self.categories = categories
        self.entities = entities

    def add_zero_category(self, category_name: str):
        self.categories.append(Category(category_name, 0.))

    def get_categories_train(self):
        return self.document, {'cats': {category.name: category.confidence for category in self.categories}}

    def get_entities_train(self):
        return self.document, {'entities': [entity.train_form() for entity in self.entities]}


class NLPModel:
    def __init__(self, samples: List[Sample] = None):
        if samples is None:
            samples = []
        self.samples = samples

    def __iter__(self):
        for x in self.samples:
            yield x

    def get_all_categories(self) -> Set[Category]:
        """Retrieves all categories present in the model"""
        all_categories = set([])
        for sample in self.samples:
            for cat in sample.categories:
                all_categories.add(cat.name)
        return all_categories

    def get_all_entities(self) -> Set[NamedEntity]:
        """Retrieves all entities present in the model"""
        all_entities = set([])
        for sample in self.samples:
            for ent in sample.entities:
                all_entities.add(ent.value)
        return all_entities
