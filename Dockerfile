# syntax=docker/dockerfile:experimental
FROM python:3.8.0-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add build-base \
        && apk add gcc postgresql-dev python3-dev musl-dev jpeg-dev zlib-dev \
        && pip install --upgrade pip

COPY ./requirements /app/requirements
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements/dev.txt

COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh

RUN mkdir -p /var/run/celery
RUN addgroup app \
        && adduser --disabled-password --gecos "" --ingroup app --no-create-home app \
        && chown app:app /var/run/celery

USER app

ENTRYPOINT ["/app/entrypoint.sh"]
