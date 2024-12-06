# Installation

## Prerequisites
- Python 3.11+
- Pip (Python Package Manager)
- Virtualenv
- Git

## Steps to Install
Clone the repository:
```bash
git clone https://github.com/rishbot91/todo-project.git
cd todo_project
```
Set up a virtual environment:
```bash
python -m venv env
source env/bin/activate  # For Linux/Mac
env\Scripts\activate  # For Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Apply migrations:
```bash
python manage.py migrate
```

Create a superuser:
```bash
python manage.py createsuperuser
```

Run the development server:
```bash
python manage.py runserver
```

Access the app at http://127.0.0.1:8000/