from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from todo_app.models import TodoItem, Tag
from django.contrib.auth.models import User
import base64


class TodoItemAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user for Basic Authentication
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Generate the Basic Authentication header
        credentials = base64.b64encode(b"testuser:testpass").decode("utf-8")
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Basic {credentials}"}

        # Create initial data
        self.tag = Tag.objects.create(name="Work")
        self.todo = TodoItem.objects.create(
            title="Complete assignment",
            description="Finish the Django assignment.",
            due_date=timezone.now() + timezone.timedelta(days=1),
            status="OPEN",
        )
        self.todo.tags.add(self.tag)

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_get_todo_list(self):
        url = reverse("todo-list-create")
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_todo_item(self):
        data = {
            "title": "Read book",
            "description": "Read 'Clean Code' book.",
            "due_date": (timezone.now() + timezone.timedelta(days=3)).isoformat(),
            "status": "OPEN",
            "tags": [{"name": "Reading"}],
        }
        response = self.client.post(
            reverse("todo-list-create"), data, format="json", **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)

        new_todo = TodoItem.objects.get(title="Read book")
        self.assertEqual(new_todo.description, "Read 'Clean Code' book.")
        self.assertEqual(new_todo.status, "OPEN")
        self.assertEqual(new_todo.tags.count(), 1)
        self.assertEqual(new_todo.tags.first().name, "Reading")

    def test_get_todo_detail(self):
        url = reverse("todo-detail", args=[self.todo.id])
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Complete assignment")

    def test_update_todo_item(self):
        data = {
            "title": "Complete assignment updated",
            "description": "Updated description.",
            "due_date": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            "status": "WORKING",
            "tags": [{"name": "Updated Tag"}],
        }
        response = self.client.put(
            reverse("todo-detail", args=[self.todo.id]),
            data,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        updated_todo = TodoItem.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.title, "Complete assignment updated")
        self.assertEqual(updated_todo.status, "WORKING")
        self.assertEqual(updated_todo.tags.count(), 1)
        self.assertEqual(updated_todo.tags.first().name, "Updated Tag")

    def test_delete_todo_item(self):
        url = reverse("todo-detail", args=[self.todo.id])
        response = self.client.delete(url, **self.auth_headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(TodoItem.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse("todo-list-create"))
        self.assertEqual(response.status_code, 401)
