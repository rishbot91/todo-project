from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from todo_app.models import TodoItem, Tag
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import base64


class TodoItemIntegrationTest(TestCase):
    def setUp(self):
        # Setup client and Basic Authentication
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        credentials = base64.b64encode(b"testuser:testpass").decode("utf-8")
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Basic {credentials}"}

        # Create initial data
        self.tag = Tag.objects.create(name="Work")
        self.todo = TodoItem.objects.create(
            title="Complete assignment",
            description="Finish the integration test assignment.",
            due_date=timezone.now() + timezone.timedelta(days=1),
            status="OPEN",
        )
        self.todo.tags.add(self.tag)

    def test_clean_method_direct(self):
        """Test the clean method directly for a past due_date."""
        todo = TodoItem(
            title="Direct Clean Test",
            description="This task has a past due_date.",
            due_date=timezone.now() - timezone.timedelta(days=1),
            status="OPEN",
        )
        with self.assertRaises(ValidationError) as context:
            todo.clean()
        self.assertIn("Due date cannot be in the past.", str(context.exception))

    def test_todo_item_clean_method_valid_due_date(self):
        """Test creating a TodoItem with a valid due_date via API."""
        create_url = reverse("todo-list-create")
        create_data = {
            "title": "Valid Due Date Task",
            "description": "This task has a valid due_date.",
            "due_date": (timezone.now() + timezone.timedelta(days=3)).isoformat(),
            "status": "OPEN",
            "tags": [{"name": "Work"}],
        }
        response = self.client.post(
            create_url, create_data, format="json", **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Valid Due Date Task")

    def test_todo_item_clean_method_invalid_due_date(self):
        """Test creating a TodoItem with an invalid due_date (past) via API."""
        create_url = reverse("todo-list-create")
        create_data = {
            "title": "Invalid Due Date Task",
            "description": "This task has a past due_date.",
            "due_date": (timezone.now() - timezone.timedelta(days=3)).isoformat(),
            "status": "OPEN",
            "tags": [{"name": "Work"}],
        }
        response = self.client.post(
            create_url, create_data, format="json", **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("due_date", response.data)
        self.assertIn("Due date cannot be in the past.", str(response.data))

    def test_tag_str_method(self):
        """Test the string representation of the Tag model."""
        self.assertEqual(str(self.tag), "Work")

    def test_todo_item_str_method(self):
        """Test the string representation of the TodoItem model."""
        self.assertEqual(str(self.todo), "Complete assignment")

    def test_duplicate_tags_in_todo_item(self):
        """Test that duplicate tags cannot be added to a TodoItem."""
        create_url = reverse("todo-list-create")
        create_data = {
            "title": "Task with Duplicate Tags",
            "description": "This task has duplicate tags.",
            "due_date": (timezone.now() + timezone.timedelta(days=3)).isoformat(),
            "status": "OPEN",
            "tags": [{"name": "Tag1"}, {"name": "Tag1"}],
        }
        create_response = self.client.post(
            create_url, create_data, format="json", **self.auth_headers
        )
        self.assertEqual(create_response.status_code, 400)
        self.assertIn("Duplicate tags are not allowed", str(create_response.data))

    def test_todo_item_full_workflow(self):
        """Test the full CRUD workflow for TodoItem without duplicate tags."""
        create_url = reverse("todo-list-create")
        create_data = {
            "title": "Integration Test Task",
            "description": "This is a test for the integration workflow.",
            "due_date": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "status": "OPEN",
            "tags": [{"name": "Integration"}, {"name": "Workflow"}],
        }
        create_response = self.client.post(
            create_url, create_data, format="json", **self.auth_headers
        )
        self.assertEqual(create_response.status_code, 201)

        todo_id = create_response.data["id"]
        detail_url = reverse("todo-detail", args=[todo_id])
        detail_response = self.client.get(detail_url, **self.auth_headers)
        self.assertEqual(detail_response.status_code, 200)

        update_data = {
            "title": "Updated Integration Test Task",
            "description": "Updated description.",
            "due_date": (timezone.now() + timezone.timedelta(days=3)).isoformat(),
            "status": "WORKING",
            "tags": [{"name": "Updated"}, {"name": "Workflow"}],
        }
        update_response = self.client.put(
            detail_url, update_data, format="json", **self.auth_headers
        )
        self.assertEqual(update_response.status_code, 200)

        verify_response = self.client.get(detail_url, **self.auth_headers)
        self.assertEqual(verify_response.data["title"], "Updated Integration Test Task")

        delete_response = self.client.delete(detail_url, **self.auth_headers)
        self.assertEqual(delete_response.status_code, 204)

        confirm_response = self.client.get(detail_url, **self.auth_headers)
        self.assertEqual(confirm_response.status_code, 404)

    def test_todo_item_update_invalid_due_date(self):
        """Test updating a TodoItem to have an
        invalid due_date (past) via API."""
        todo_id = self.todo.id
        detail_url = reverse("todo-detail", args=[todo_id])
        update_data = {
            "title": self.todo.title,
            "description": self.todo.description,
            "due_date": (timezone.now() - timezone.timedelta(days=1)).isoformat(),
            "status": self.todo.status,
            "tags": [{"name": "Work"}],
        }
        response = self.client.put(
            detail_url, update_data, format="json", **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("due_date", response.data)

    def test_todo_item_tag_reuse(self):
        """Test that tags are reused across different TodoItems."""
        Tag.objects.create(name="Reusable Tag")
        create_url = reverse("todo-list-create")
        create_data = {
            "title": "Task with Existing Tag",
            "description": "Testing tag reuse.",
            "due_date": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            "status": "OPEN",
            "tags": [{"name": "Reusable Tag"}],
        }
        create_response = self.client.post(
            create_url, create_data, format="json", **self.auth_headers
        )
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(Tag.objects.filter(name="Reusable Tag").count(), 1)

    def test_home_view(self):
        """Test the home view renders the correct template."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
