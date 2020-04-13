# syntax=docker/dockerfile:experimental
FROM python:3.8.0-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN apk update \
        && apk add build-base \
        && apk add gcc postgresql-dev python3-dev musl-dev jpeg-dev zlib-dev \
        && pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY ./entry-point.sh /app/entry-point.sh

COPY . /app
COPY ./entry-point.sh /app/entry-point.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/app/entry-point.sh"]
