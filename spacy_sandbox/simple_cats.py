import spacy

train_data = [
    (u"quelle heure il est", {"cats": {"GET_TIME": 1, "HELLO": 0, "LAST_SHOWTIME": 0}}),
    (u"c'est quoi l'heure", {"cats": {"GET_TIME": 1, "HELLO": 0, "LAST_SHOWTIME": 0}}),
    (u"j'ai besoin de connaître l'heure", {"cats": {"GET_TIME": 1, "HELLO": 0, "LAST_SHOWTIME": 0}}),
    (u"aurais-tu une idée de l'heure qu'il est", {"cats": {"GET_TIME": 1, "HELLO": 0, "LAST_SHOWTIME": 0}}),

    (u"bonjour", {"cats": {"GET_TIME": 0, "HELLO": 1, "LAST_SHOWTIME": 0}}),
    (u"salut", {"cats": {"GET_TIME": 0, "HELLO": 1, "LAST_SHOWTIME": 0}}),
    (u"hello", {"cats": {"GET_TIME": 0, "HELLO": 1, "LAST_SHOWTIME": 0}}),
    (u"salutations", {"cats": {"GET_TIME": 0, "HELLO": 1, "LAST_SHOWTIME": 0}}),

    (u"il y a quoi au cinéma", {"cats": {"GET_TIME": 0, "HELLO": 0, "LAST_SHOWTIME": 1}}),
    (u"qu'est ce qu'il y a au ciné ce soir", {"cats": {"GET_TIME": 0, "HELLO": 0, "LAST_SHOWTIME": 1}}),
    (u"programme ciné", {"cats": {"GET_TIME": 0, "HELLO": 0, "LAST_SHOWTIME": 1}}),

    (u"ajoute des pâtes à ma liste", {"cats": {"ADD_TO_LIST": 1}}),
    (u"ajoute des tomates à ma liste de courses", {"cats": {"ADD_TO_LIST": 1}}),

]


all_categories = set([])
for doc, gold in train_data:
    for cat_key, cat_val in gold['cats'].items():
        all_categories.add(cat_key)
for doc, gold in train_data:
    for cat in all_categories:
        if cat not in gold['cats']:
            gold['cats'][cat] = 0


nlp = spacy.load('fr_core_news_md')
textcat = nlp.create_pipe('textcat')
nlp.add_pipe(textcat, last=True)
for cat in all_categories:
    textcat.add_label(cat)
optimizer = nlp.begin_training()
for itn in range(5):
    for doc, gold in train_data:
        nlp.update([doc], [gold], sgd=optimizer)
doc = nlp(u"t'as pas l'heure s'il te plaît")
print(doc.cats)
doc = nlp(u'bonjour à vous')
print(doc.cats)
doc = nlp(u'horaires de ciné')
print(doc.cats)
nlp.to_disk("../data")