# General commands
pre-commit-run = pre-commit run --all-files
docker-compose = docker compose -f local.yml

# Build and run
.build = docker-compose up --build -d --remove-orphans
.up = docker-compose up -d
.down = docker-compose down
.show-logs = docker-compose logs
.show-logs-api = docker-compose logs server

# Database management
.volume = docker volume inspect local_postgres_data
.djinni-db = docker-compose exec postgres psql --username=mafan --dbname=djinni-live

# Django management commands
.backend = cd backend &&
.collectstatic = .backend python manage.py collectstatic --no-input --clear
.createsuperuser = .backend python manage.py createsuperuser
.makemigrations = .backend python manage.py makemigrations
.migrate = .backend python manage.py migrate

# Testing
.cov = docker-compose run --rm server pytest -p no:warnings --cov=. -v
.cov-gen = docker-compose run --rm server pytest -p no:warnings --cov=. --cov-report html
.tests = docker-compose run --rm server pytest
