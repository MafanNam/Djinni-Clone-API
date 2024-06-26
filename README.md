# Djinni-Clone-API

This is the repository for the Djinni-Clone-API project, which is a clone of the Djinni web service. This API implements
a basic set of functionalities allowing users to interact with the platform.

![Djinni title](https://raw.githubusercontent.com/MafanNam/Djinni-Clone-API/dev-0.4/screanshots/title.svg)

### Diagram DB

![Djinni diagram DB](https://raw.githubusercontent.com/MafanNam/Djinni-Clone-API/dev-0.4/screanshots/djinni_clone_diagram_db.svg)

## Description

Djinni-Clone-API is developed using Django, one of the most popular frameworks for building web applications in Python.
This API provides features such as user registration, advertisement creation, user profile management, and other core
functionalities.

![Djinni frontend](https://raw.githubusercontent.com/MafanNam/Djinni-Clone-API/dev-0.4/screanshots/frontend.gif)

## Requirements

To run this API, you'll need:

- Python 3.11
- Django
- Django REST Framework
- and other dependencies listed in the `requirements.txt` file

## Installation and Running

1. Clone the repository to your local machine:

```bash
$ git clone https://github.com/MafanNam/Djinni-Clone-API.git
```

2. Navigate to the project directory:

```bash
$ cd Djinni-Clone-API
```

3. Create/Activate environment:

```bash
$ pip install virtualenv
$ python -m virtualenv venv
$ .\venv\Scripts\activate
$ # or linux
$ source venv/bin/activate
```

4. Install dependencies:

```bash
$ pip install -r requirements.txt
```

5. Navigate to api directory:

```bash
$ cd backend
```

6. Apply migrations to create the database:

```bash
$ python manage.py migrate
```

7. Load example data

```bash
$ python -Xutf8 ./manage.py loaddata mydata.json
```

8. Run the server:

```bash
$ python manage.py runserver
```

#### About fixtures(mydata.json)

All user email in [mydata.json](backend/mydata.json) and `password=Pass12345`

for admin user `email=admin@gmail.com` and `password=1`

### If you want the api to send messages to mail

Then you MUST create and config `django.env` optional `django.docker.env`.

For example I create `django.example.env` and `django.docker.example.env`

All these files are in [.envs/.local/](.envs/.local/)

You can now access the API in your browser at http://localhost:8000/.

## Getting Started with Docker

Commands can be run through a makefile or written manually.

You can access the API in your browser at http://localhost:8080/. Flower http://localhost:5555/

### To build and raise a container, you just need to run it:

You cannot use makefile

```bash
$ docker compose -f local.yml up --build -d --remove-orphans
$ # or
$ docker compose -f local.yml up --build
```

You can use makefile

```bash
$ make build
$ # or
$ make build-log
```

### Basic commands:

```bash
$ make buld-log

$ make up

$ make down
```

## Run test

For testing

#### makefile

```bash
$ make tests
```

#### no makefile

```bash
$ docker compose -f local.yml run --rm server python manage.py test
```

## API Documentation

The API documentation is not available [localhost:8080](http://localhost:8080).

![Djinni endpoints](https://raw.githubusercontent.com/MafanNam/Djinni-Clone-API/dev-0.4/screanshots/endpoints.gif)

## Author

This project is developed by Mafan.

## License

This project is licensed under MIT License.
