from python:3.10-slim-buster

RUN mkdir /code
RUN apt update && apt install -y libreoffice
RUN pip install --upgrade pip && pip install celery redis watchdog fire

WORKDIR /code
COPY celeryconfig.py .
COPY worker worker
COPY  odt_to_pdf  odt_to_pdf

ENV CELERY_CONFIG_MODULE=celeryconfig
ENV CELERY_QUEUE_NAME=odt_to_pdf
ENV CELERY_DEBUG_LEVEL=INFO

CMD celery -A worker worker -Q $CELERY_QUEUE_NAME -l $CELERY_DEBUG_LEVEL

