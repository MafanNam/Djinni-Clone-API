#!/bin/sh

set -e # exit immediately if any command exits with a non-zero status

# wait for server volume and cd into /app/backend
until cd /app/backend
do
    echo "Waiting for server volume..."
    sleep 1
done

# wait for db to be ready
until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 5
done

# display the current working directory
pwd

# run a worker celery beat with logging and signal handling
celery -A backend.celery beat -l info --pidfile=/var/run/celery/celerybeat.pid --signalfile=/var/run/celery/celerybeat.pid.signal \
    --beat-schedule=/app/backend/celerybeat-schedule --max-interval=300

