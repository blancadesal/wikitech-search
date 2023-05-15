# First stage: requirements
FROM python:3.11-slim-bullseye as requirements-stage

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Second stage: build
FROM python:3.11-slim-bullseye

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt && \
    rm /code/requirements.txt

COPY ./app /code/app
