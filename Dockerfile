FROM python:3.10

LABEL maintainer="celian.garcia1@gmail.com"

# Some arguments used for labelling
ARG BUILD_DATE
ARG VCS_REF
ARG BUILD_VERSION
ARG PROJECT_NAME
ARG MODULE_NAME
ARG MODULE_DESCRIPTION
ARG DOCKER_IMAGE

# Labels.
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="$PROJECT_NAME::$MODULE_NAME"
LABEL org.label-schema.description=$MODULE_DESCRIPTION
LABEL org.label-schema.url="https://www.$PROJECT_NAME.com/"
LABEL org.label-schema.vcs-url="https://github.com/$PROJECT_NAME/$MODULE_NAME"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.version=$BUILD_VERSION
LABEL org.label-schema.docker.cmd="docker run -it $DOCKER_IMAGE:$BUILD_VERSION"

COPY . /src
WORKDIR /src

# Install cerebro module and dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

# Download the spacy base model
RUN python -m spacy download fr_core_news_md

# Build the main command
CMD ["sanic", "cerebro.server.app", "--host=0.0.0.0", "--port=9444"]
