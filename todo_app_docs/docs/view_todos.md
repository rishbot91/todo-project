# View All Todos

This endpoint retrieves all todo items.

---

## **Endpoint**
- **URL:** `/api/todos/`
- **Method:** GET

---

## **Response**

### Success (200 OK):
```json
[
  {
    "id": 1,
    "timestamp": "2024-12-06T12:00:00Z",
    "title": "First Task",
    "description": "Details about the first task.",
    "due_date": "2024-12-10T10:00:00Z",
    "tags": [
      {"id": 1, "name": "Work"}
    ],
    "status": "OPEN"
  },
  {
    "id": 2,
    "timestamp": "2024-12-07T12:00:00Z",
    "title": "Second Task",
    "description": "Details about the second task.",
    "due_date": "2024-12-11T10:00:00Z",
    "tags": [],
    "status": "WORKING"
  }
]
```
Each object in the array represents a single todo item.