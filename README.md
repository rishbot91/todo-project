# Todo List App

A backend web-based Todo List application built using Django and Django REST Framework. This application allows users to create, read, update, and delete (CRUD) Todo items while supporting features like authentication, tagging, and status management.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete Todo items.
- **Authentication**: Basic Authentication for all APIs.
- **Tagging System**: Add one or more tags to each Todo item.
- **Status Management**: Predefined statuses (OPEN, WORKING, etc.).
- **Admin Panel**: Full control over Todo items and tags via the Django Admin interface.
- **Test Coverage**: 100% Unit and Integration test coverage.
- **E2E Testing**: Automated end-to-end testing using Selenium.
- **CI/CD Integration**: Automated testing and linting via GitHub Actions.

---

## Tech Stack

- **Language**: Python 3.11+
- **Frameworks**: Django 5.1.3, Django REST Framework 3.15.2
- **Testing**: Selenium for E2E tests, Django's `TestCase` for Unit and Integration tests
- **CI/CD**: GitHub Actions
- **Hosting**: PythonAnywhere for app deployment, GitHub Pages for documentation

---

## Requirements

1. Python 3.11+
2. Django 5.1.3
3. PostgreSQL (or SQLite for local development)
4. Git for version control

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/todo-project.git
cd todo-project
```

### 2. Create a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup the Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser
```bash
python manage.py createsuperuser
```

### Run the Server
```bash
python manage.py runserve
```

## API Endpoints
| Method | Endpoint           | Description            |
|--------|--------------------|------------------------|
| GET    | `/api/todos/`      | List all Todo items    |
| POST   | `/api/todos/`      | Create a new Todo item |
| PUT    | `/api/todos/<id>/` | Update a Todo item     |
| DELETE | `/api/todos/<id>/` | Delete a Todo item     |

## Running Unit Tests and Integration tests
### 1. Run Unit Tests
```bash
coverage run --source='.' --omit='manage.py,config/asgi.py,config/wsgi.py,todo_app/tests/test_e2e/*,todo_app/tests/test_integration/*' manage.py test todo_app.tests.test_unit
```

### 2. Generate Coverage Reports for unit test
```bash
coverage report -m
coverage html -d covhtml_unit
```

### 3. Run integration Tests
```bash
coverage run --source='.' --omit='manage.py,config/asgi.py,config/wsgi.py,todo_app/tests/test_e2e/*,todo_app/tests/test_unit/*' manage.py test todo_app.tests.test_integration
```

### 4. Generate Coverage Reports for integration test
```bash
coverage report -m
coverage html -d covhtml_integration
```

## Coverage Summary screenshots

![Unit Test Coverage Summary Screenshot](coverage_screenshots\unit_test_report.png "unit_test_report")

![Unit Test Coverage Summary Screenshot](coverage_screenshots\integration_test_report.png "integration_test_report")

## Open Coverage Reports
### 1. Open unit test report:
```bash
open covhtml_unit/index.html
```
### 1. Open integration test report:
```bash
open covhtml_integration/index.html
```

## Deployment
### 1. Host the App
The application is hosted on PythonAnywhere:

### 2. Documentation
Documentation is hosted on GitHub Pages:

## Superuser Credentials
For the admin panel:
```bash
Username: admin
Password: admin@13579
```


