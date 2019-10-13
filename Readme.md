# Cerebro

Cerebro manage the NLU (Natural Language Understanding) part of Milobella.

## Installation
```bash
python -m spacy download fr
python -m spacy download fr_core_news_md
pip install -r requirements.txt
pip install -e .
```

## Update the learning sentences
Update the spacy_sandbox/simple_cats.py file with the new sentences and categories.

```bash
python spacy_sandbox/simple_cats.py
```

It might take a few minutes.

## Run
```bash
$ python manage.py runserver --config-file cerebro.ini
```

## Upload and train a model
When the server is running, this is not over. You have two tasks to perform to make it work.

#### Upload the model (not necessary if the model is already in database)
```bash
$ curl -iv -X PUT 'http://localhost:9444/models/default/samples' -d @samples.json
```
An example of ``samples.json`` file format is here : [./scripts/samples.json](./scripts/samples.json)

#### Train the model (necessary after each server start and after each upload)
```bash
$ curl -iv -X POST 'http://localhost:9444/models/default/train'
```

## Request example
```bash
$ curl -iv http://localhost:9444/understand?query="Bonjour"
```

## CHANGELOGS
- [Application changelog](./CHANGELOG.md)
- [Helm chart changelog](./helm/cerebro/CHANGELOG.md)
