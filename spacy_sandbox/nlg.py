# import spacy
# nlp = spacy.load('fr')

import fr_core_news_md

nlp = fr_core_news_md.load()

# train_data = [
#     (u"quelle heure il est", {"cats": {"GET_TIME": 1, "HELLO": 0}}),
#     (u"c'est quoi l'heure", {"cats": {"GET_TIME": 1, "HELLO": 0}}),
#     (u"j'ai besoin de connaître l'heure", {"cats": {"GET_TIME": 1, "HELLO": 0}}),
#     (u"aurais-tu une idée de l'heure qu'il est", {"cats": {"GET_TIME": 1, "HELLO": 0}}),
#
#     (u"bonjour", {"cats": {"GET_TIME": 0, "HELLO": 1}}),
#     (u"salut", {"cats": {"GET_TIME": 0, "HELLO": 1}}),
#     (u"hello", {"cats": {"GET_TIME": 0, "HELLO": 1}}),
#     (u"salutations", {"cats": {"GET_TIME": 0, "HELLO": 1}}),
# ]
#
# textcat = nlp.create_pipe('textcat')
# nlp.add_pipe(textcat, last=True)
# textcat.add_label('GET_TIME')
# textcat.add_label('HELLO')
# optimizer = nlp.begin_training()
# for itn in range(5):
#     for doc, gold in train_data:
#         nlp.update([doc], [gold], sgd=optimizer)
doc = nlp(u"t'as pas l'heure s'il te plaît")
print(doc.cats)
doc = nlp(u'bonjour à vous')
print(doc.cats)
#
# nlp.to_disk("../data")