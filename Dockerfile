FROM python:3.7

WORKDIR /app
COPY . /app

# Install cerebro module and dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

# Download the spacy base model
RUN python -m spacy download fr_core_news_md

CMD ["python", "manage.py", "runserver"]