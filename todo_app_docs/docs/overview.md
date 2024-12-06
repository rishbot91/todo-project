
# API Overview

Base URL: `http://127.0.0.1:8000/api/`

## Endpoints

### Create a Task
- **Method:** POST
- **URL:** `/todos/`
- **Body:**

```json
    {
        "title": "New Task",
        "description": "Complete this task",
        "due_date": "2024-12-10T10:00:00Z",
        "tags": [{"name": "Work"}, {"name": "Urgent"}],
        "status": "OPEN"
    }
```
