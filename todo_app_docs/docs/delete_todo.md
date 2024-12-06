# Delete a Todo Item

This endpoint deletes a specific todo item.

---

## **Endpoint**
- **URL:** `/api/todos/<task_id>/`
- **Method:** DELETE

---

## **Response**

### Success (204 No Content):
No body is returned. The todo item is successfully deleted.

---

## **Errors**

### Not Found (404):
If the specified `task_id` does not exist:
```json
{
  "error": "Todo item not found."
}