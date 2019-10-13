from typing import List, Dict

from cerebro.repository.nlp_repository import Repository


class NLPRepositoryFake(Repository):
    def __init__(self):
        self._database = [
            {
                "text": "quelle heure il est",
                "categories": [
                    "GET_TIME"
                ]
            },
            {
                "text": "c'est quoi l'heure",
                "categories": [
                    "GET_TIME"
                ]
            },
            {
                "text": "j'ai besoin de connaître l'heure",
                "categories": [
                    "GET_TIME"
                ]
            },
            {
                "text": "aurais-tu une idée de l'heure qu'il est",
                "categories": [
                    "GET_TIME"
                ]
            },
            {
                "text": "bonjour",
                "categories": [
                    "HELLO"
                ]
            },
            {
                "text": "salut",
                "categories": [
                    "HELLO"
                ]
            },
            {
                "text": "hello",
                "categories": [
                    "HELLO"
                ]
            },
            {
                "text": "salutations",
                "categories": [
                    "HELLO"
                ]
            },
            {
                "text": "il y a quoi au cinéma",
                "categories": [
                    "LAST_SHOWTIME"
                ]
            },
            {
                "text": "qu'est ce qu'il y a au ciné ce soir",
                "categories": [
                    "LAST_SHOWTIME"
                ]
            },
            {
                "text": "programme ciné",
                "categories": [
                    "LAST_SHOWTIME"
                ]
            },
            {
                "text": "je veux écouter Michael Jackson",
                "categories": [
                    "PLAY_MUSIC"
                ],
                "entities": [
                    {
                        "start": 16,
                        "end": 23,
                        "name": "MUSIC_CONTENT"
                    }
                ]
            },
            {
                "text": "mets de la musique",
                "categories": [
                    "PLAY_MUSIC"
                ]
            },
            {
                "text": "écouter Metallica",
                "categories": [
                    "PLAY_MUSIC"
                ],
                "entities": [
                    {
                        "start": 8,
                        "end": 17,
                        "name": "MUSIC_CONTENT"
                    }
                ]
            },
            {
                "text": "je veux écouter de la musique",
                "categories": [
                    "PLAY_MUSIC"
                ]
            },
            {
                "text": "on fait la liste de courses",
                "categories": [
                    "TRIGGER_SHOPPING_LIST"
                ]
            },
            {
                "text": "c'est parti pour la liste de courses",
                "categories": [
                    "TRIGGER_SHOPPING_LIST"
                ]
            },
            {
                "text": "faisons les courses",
                "categories": [
                    "TRIGGER_SHOPPING_LIST"
                ]
            },
            {
                "text": "on peut faire la liste de courses",
                "categories": [
                    "TRIGGER_SHOPPING_LIST"
                ]
            },
            {
                "text": "ajoute des pâtes à ma liste",
                "categories": [
                    "ADD_TO_LIST"
                ],
                "entities": [
                    {
                        "start": 11,
                        "end": 16,
                        "name": "SHOPITEM"
                    }
                ]
            },
            {
                "text": "ajoute des tomates à ma liste de courses",
                "categories": [
                    "ADD_TO_LIST"
                ],
                "entities": [
                    {
                        "start": 11,
                        "end": 18,
                        "name": "SHOPITEM"
                    }
                ]
            },
            {
                "text": "ajoute du beurre de cacahuètes à ma liste de courses",
                "categories": [
                    "ADD_TO_LIST"
                ],
                "entities": [
                    {
                        "start": 10,
                        "end": 30,
                        "name": "SHOPITEM"
                    }
                ]
            },
            {
                "text": "mets un minuteur de 10 minutes",
                "categories": [
                    "SET_TIMER"
                ]
            },
            {
                "text": "mets un timer de 15 minutes",
                "categories": [
                    "SET_TIMER"
                ]
            },
            {
                "text": "quel temps il fait à Paris",
                "categories": [
                    "GET_WEATHER"
                ]
            },
            {
                "text": "donne-moi la météo",
                "categories": [
                    "GET_WEATHER"
                ]
            },
            {
                "text": "météo",
                "categories": [
                    "GET_WEATHER"
                ]
            },
            {
                "text": "quel temps fait-il",
                "categories": [
                    "GET_WEATHER"
                ]
            }
        ]
        self._categories = [
            "GET_TIME",
            "HELLO",
            "LAST_SHOWTIME",
            "PLAY_MUSIC",
            "TRIGGER_SHOPPING_LIST",
            "PLAY_MUSIC",
            "ADD_TO_LIST",
            "SET_TIMER",
            "GET_WEATHER",
        ]

        self._entities = [
            "MUSIC_CONTENT",
            "SHOPITEM"
        ]

    def get_samples(self, model_id: str, start: int, limit: int) -> List[Dict]:
        return self._database[start: start + limit]

    def get_categories(self, model_id: str) -> List[str]:
        return self._categories

    def get_entities(self, model_id: str) -> List[str]:
        return self._entities

    def update(self, model_id: str, samples: List[Dict]):
        pass

    def clear(self, model_id: str):
        pass
