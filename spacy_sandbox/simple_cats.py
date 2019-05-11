import random

import spacy
from spacy.util import compounding, minibatch

TRAIN_DATA = [
    (u"quelle heure il est", {"cats": {"GET_TIME": 1}}),
    (u"c'est quoi l'heure", {"cats": {"GET_TIME": 1}}),
    (u"j'ai besoin de connaître l'heure", {"cats": {"GET_TIME": 1}}),
    (u"aurais-tu une idée de l'heure qu'il est", {"cats": {"GET_TIME": 1}}),

    (u"bonjour", {"cats": {"HELLO": 1}}),
    (u"salut", {"cats": {"HELLO": 1}}),
    (u"hello", {"cats": {"HELLO": 1}}),
    (u"salutations", {"cats": {"HELLO": 1}}),

    (u"il y a quoi au cinéma", {"cats": {"LAST_SHOWTIME": 1}}),
    (u"qu'est ce qu'il y a au ciné ce soir", {"cats": {"LAST_SHOWTIME": 1}}),
    (u"programme ciné", {"cats": {"LAST_SHOWTIME": 1}}),

    (u"ajoute des pâtes à ma liste", {
        "cats": {"ADD_TO_LIST": 1},
        'entities': [(11, 16, 'SHOPITEM')]
    }),
    (u"ajoute des tomates à ma liste de courses", {
        "cats": {"ADD_TO_LIST": 1},
        'entities': [(11, 18, 'SHOPITEM')]
    }),
    (u"on fait la liste de courses", {"cats": {"TRIGGER_SHOPPING_LIST": 1}}),
    (u"c'est parti pour la liste de courses", {"cats": {"TRIGGER_SHOPPING_LIST": 1}}),
    (u"faisons les courses", {"cats": {"TRIGGER_SHOPPING_LIST": 1}}),
    (u"on peut faire la liste de courses", {"cats": {"TRIGGER_SHOPPING_LIST": 1}}),
]

ENTITIES = ['SHOPITEM']

ITERATIONS = 40


def train_ner(nlp, all_entities, train_entities_data):
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    for entity in all_entities:
        ner.add_label(entity)

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(ITERATIONS):
            random.shuffle(train_entities_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_entities_data, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print('Losses', losses)


def train_categories(nlp, all_categories, train_categories_data):
    # add the text classifier to the pipeline if it doesn't exist
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'textcat' not in nlp.pipe_names:
        textcat = nlp.create_pipe('textcat')
        nlp.add_pipe(textcat, last=True)
    # otherwise, get it, so we can add labels to it
    else:
        textcat = nlp.get_pipe('textcat')

    for cat in all_categories:
        textcat.add_label(cat)

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        optimizer = nlp.begin_training()
        # print("Training the model...")
        # print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))

        for itn in range(ITERATIONS):
            losses = {}
            batches = minibatch(train_categories_data, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, losses=losses)

            # with textcat.model.use_params(optimizer.averages):
            #     # evaluate on the dev data split off in load_data()
            #     scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
            # print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
            #       .format(losses['textcat'], scores['textcat_p'],
            #               scores['textcat_r'], scores['textcat_f']))


def main():
    all_categories = set([])
    for doc, annotation in TRAIN_DATA:
        if 'cats' in annotation:
            for cat_key, cat_val in annotation['cats'].items():
                all_categories.add(cat_key)

    for doc, annotation in TRAIN_DATA:
        for cat in all_categories:
            if 'cats' in annotation and cat not in annotation['cats']:
                annotation['cats'][cat] = 0

    train_categories_data = []
    train_entities_data = []
    for doc, annotation in TRAIN_DATA:
        if 'cats' in annotation:
            train_categories_data.append((doc, {'cats': annotation["cats"]}))
        if 'entities' in annotation:
            train_entities_data.append((doc, {'entities': annotation["entities"]}))

    nlp = spacy.load('fr_core_news_md')

    train_categories(nlp, all_categories, train_categories_data)

    train_ner(nlp, ENTITIES, train_entities_data)

    doc = nlp(u"t'as pas l'heure s'il te plaît")
    print(doc.cats)
    doc = nlp(u'bonjour à vous')
    print(doc.cats)
    doc = nlp(u'horaires de ciné')
    print(doc.cats)

    # Save trained NLP
    nlp.to_disk("data")


if __name__ == '__main__':
    main()
