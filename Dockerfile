FROM python:3.7

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN python -m spacy download fr_core_news_md
RUN python spacy_sandbox/simple_cats.py
RUN pip install .


CMD ["cerebro"]