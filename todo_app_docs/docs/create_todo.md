# Create a Todo Item

This endpoint allows you to create a new todo item.

## **Endpoint**
- **URL:** `/api/todos/`
- **Method:** POST

## **Request Body**
Provide the details of the todo item to be created:

```json
{
  "title": "New Task",
  "description": "Details about the task.",
  "due_date": "2024-12-10T10:00:00Z",
  "tags": [
    {"name": "Work"},
    {"name": "Urgent"}
  ],
  "status": "OPEN"
}
```
- **title** (string, required): The title of the task.
- **description** (string, required): Detailed description of the task.
- **due_date** (string, optional): The deadline for the task in ISO 8601 format.
- **tags** (list, optional): A list of tags associated with the task.
- **status** (string, required): The status of the task. Valid values are:
  - `OPEN`
  - `WORKING`
  - `PENDING REVIEW`
  - `COMPLETED`
  - `OVERDUE`
  - `CANCELLED`

### Response

#### Success (201 Created):
```json
{
  "id": 1,
  "timestamp": "2024-12-06T12:00:00Z",
  "title": "New Task",
  "description": "Details about the task.",
  "due_date": "2024-12-10T10:00:00Z",
  "tags": [
    {"id": 1, "name": "Work"},
    {"id": 2, "name": "Urgent"}
  ],
  "status": "OPEN"
}
```
### Errors
#### Bad Request (400):

- Missing required fields.
- Invalid status or due date in the past.

Example:

```json
{
  "error": "Due date cannot be in the past."
}
```






