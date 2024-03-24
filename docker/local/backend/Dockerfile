# pull official base image
FROM python:3.11-alpine3.15
LABEL maintainer="Your Name"

# install system dependencies
RUN apk update && apk add --no-cache python3-dev gcc libc-dev musl-dev

# set the working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# upgrade pip and install required packages
RUN pip install --upgrade pip && pip install gunicorn

# copy only the necessary files for requirements.txt
COPY ./requirements/local.txt /app/requirements.txt
COPY ./requirements/base.txt /app/base.txt

# install python dependencies
RUN pip install -r requirements.txt

# remove the sed -i command as it's not a good practice to modify the installed packages
# RUN sed -i '/def _get_flatchoices(self):/,/flatchoices = property(_get_flatchoices)/d' /usr/local/lib/python3.11/site-packages/multiselectfield/db/fields.py

# copy the application code
COPY ./backend /app/backend

# copy the environment variables file
COPY .envs /app/backend/.envs

RUN chmod +x /app/docker/backend/*-entrypoint.sh

# expose the ports
EXPOSE 8000

# define the entrypoint for the container
ENTRYPOINT ["/app/docker/backend/server-entrypoint.sh"]
