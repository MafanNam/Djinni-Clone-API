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

3. Install dependencies:

```bash
$ pip install -r requirements/local.txt
```

4. Apply migrations to create the database:

```bash
$ python manage.py migrate
```

5. Run the server:

```bash
$ python manage.py runserver
```

You can now access the API in your browser at http://127.0.0.1:8000/.

## Docker in development

Not completed

## API Documentation

The API documentation is not available [localhost:8080](http://localhost:8080).

![Djinni endpoints](https://raw.githubusercontent.com/MafanNam/Djinni-Clone-API/dev-0.4/screanshots/endpoints.gif)

## Author

This project is developed by Mafan.

## License

This project is licensed under MIT License.
