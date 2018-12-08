# Installation
```bash
python -m spacy download fr
python -m spacy download fr_core_news_md
pip install -r requirements.txt
pip install -e .
```

# Update the learning sentences
Update the spacy_sandbox/simple_cats.py file with the new sentences and categories.

```bash
python spacy_sandbox/simple_cats.py
```

It might take a few minutes.

# Run
```bash
cerebro_launcher
```