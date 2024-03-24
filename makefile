clean:
	pre-commit run --all-files
build:
	docker compose -f local.yml up --build -d --remove-orphans
build-log:
	docker compose -f local.yml up --build

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f local.yml logs server

#makemigrations:
#	docker compose -f local.yml run --rm server python manage.py makemigrations
#
#migrate:
#	docker compose -f local.yml run --rm server python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm server python manage.py collectstatic --no-input --clear

createsuperuser:
	cd backend & python manage.py createsuperuser

makemigrations:
	cd backend & python manage.py makemigrations

migrate:
	cd backend & python manage.py migrate

down-v:
	docker compose -f local.yml down -v

volume:
	docker volume inspect local_postgres_data

djinni-db:
	docker compose -f local.yml exec postgres psql --username=mafan --dbname=djinni-live

cov:
	docker compose -f local.yml run --rm server pytest -p no:warnings --cov=. -v

cov-gen:
	docker compose -f local.yml run --rm server pytest -p no:warnings --cov=. --cov-report html

tests:
	docker compose -f local.yml run --rm server pytest
