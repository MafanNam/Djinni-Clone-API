# pull official base image
FROM python:3.11-alpine3.15
LABEL maintainer="Mafan"

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ./requirements/local.txt /app/requirements.txt
ADD ./requirements/base.txt /app/base.txt
RUN pip install -r requirements.txt

ADD ./backend /app/backend
ADD ./.envs /app/backend/.envs
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
RUN chmod +x /app/docker/backend/celery-beat-entrypoint.sh
