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
cerebro
```

## CHANGELOGS
- [Application changelog](./CHANGELOG.md)
- [Helm chart changelog](./helm/cerebro/CHANGELOG.md)
