from cerebro.processing.data import NLPModel, Sample, Category, NamedEntity
from cerebro.model.nlp_repository import Repository


class NLPRepositoryFake(Repository):

    def read(self) -> NLPModel:
        return NLPModel([

            # Clock
            Sample("quelle heure il est", [Category("GET_TIME")]),
            Sample("c'est quoi l'heure", [Category("GET_TIME")]),
            Sample("j'ai besoin de connaître l'heure", [Category("GET_TIME")]),
            Sample("aurais-tu une idée de l'heure qu'il est", [Category("GET_TIME")]),

            # Greetings
            Sample("bonjour", [Category("HELLO")]),
            Sample("salut", [Category("HELLO")]),
            Sample("hello", [Category("HELLO")]),
            Sample("salutations", [Category("HELLO")]),

            # Cinema
            Sample("il y a quoi au cinéma", [Category("LAST_SHOWTIME")]),
            Sample("qu'est ce qu'il y a au ciné ce soir", [Category("LAST_SHOWTIME")]),
            Sample("programme ciné", [Category("LAST_SHOWTIME")]),

            # Music
            Sample("je veux écouter Michael Jackson", [Category("PLAY_MUSIC")],
                   [NamedEntity(16, 23, 'MUSIC_CONTENT')]),
            Sample("mets de la musique", [Category("PLAY_MUSIC")]),
            Sample("écouter Metallica", [Category("PLAY_MUSIC")],
                   [NamedEntity(8, 17, 'MUSIC_CONTENT')]),
            Sample("je veux écouter de la musique", [Category("PLAY_MUSIC")]),

            # Shopping list
            Sample("on fait la liste de courses", [Category("TRIGGER_SHOPPING_LIST")]),
            Sample("c'est parti pour la liste de courses", [Category("TRIGGER_SHOPPING_LIST")]),
            Sample("faisons les courses", [Category("TRIGGER_SHOPPING_LIST")]),
            Sample("on peut faire la liste de courses", [Category("TRIGGER_SHOPPING_LIST")]),
            Sample("ajoute des pâtes à ma liste", [Category("ADD_TO_LIST")],
                   [NamedEntity(11, 16, 'SHOPITEM')]),
            Sample("ajoute des tomates à ma liste de courses", [Category("ADD_TO_LIST")],
                   [NamedEntity(11, 18, 'SHOPITEM')]),
            Sample("ajoute du beurre de cacahuètes à ma liste de courses", [Category("ADD_TO_LIST")],
                   [NamedEntity(10, 30, 'SHOPITEM')]),

            # Timer
            Sample("mets un minuteur de 10 minutes", [Category("SET_TIMER")]),
            Sample("mets un timer de 15 minutes", [Category("SET_TIMER")]),

        ])

    def update(self, entity: NLPModel) -> bool:
        pass






