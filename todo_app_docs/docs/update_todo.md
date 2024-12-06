# Update a Todo Item

This endpoint allows updating the details of an existing todo item.

---

## **Endpoint**
- **URL:** `/api/todos/<task_id>/`
- **Method:** PUT

---

## **Request Body**
Provide the updated details for the todo item:

```json
{
  "title": "Updated Task",
  "description": "Updated details about the task.",
  "due_date": "2024-12-15T10:00:00Z",
  "tags": [
    {"name": "Work"},
    {"name": "Updated"}
  ],
  "status": "WORKING"
}
```
- All fields are optional but at least one must be provided for the update.

---

### Response
#### Success (200 OK):
```json
{
  "id": 1,
  "timestamp": "2024-12-06T12:00:00Z",
  "title": "Updated Task",
  "description": "Updated details about the task.",
  "due_date": "2024-12-15T10:00:00Z",
  "tags": [
    {"id": 1, "name": "Work"},
    {"id": 3, "name": "Updated"}
  ],
  "status": "WORKING"
}
```
---

### Errors
#### Not Found (404):
- If the specified task_id does not exist:

```json
Copy code
{
  "error": "Todo item not found."
}
```

#### Bad Request (400):
- For invalid inputs like a due date in the past:

```json

{
  "error": "Due date cannot be in the past."
}
```
