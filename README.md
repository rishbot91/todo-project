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
- **Frameworks**: Django 4.2.7+, Django REST Framework 3.14.0+
- **Testing**: Selenium for E2E tests, Django's `TestCase` for Unit and Integration tests
- **CI/CD**: GitHub Actions
- **Hosting**: PythonAnywhere for app deployment, GitHub Pages for documentation

---

## Requirements

1. Python 3.11+
2. Django 4.2.7+
3. PostgreSQL (or SQLite for local development)
4. Git for version control

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/todo-project.git
cd todo-project

### 2. Create a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate

### 3. Install Dependencies
```bash
pip install -r requirements.txt

### 4. Setup the Database
```bash
python manage.py makemigrations
python manage.py migrate

### 5. Create a Superuser
```bash
python manage.py createsuperuser

### Run the Server
```bash
python manage.py runserve

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
python manage.py test todo_app.tests.test_unit todo_app.tests.test_integration

### Generate Coverage Reports
```bash
coverage run --source=todo_app manage.py test
coverage html

