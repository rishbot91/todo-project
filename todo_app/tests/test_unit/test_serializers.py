from django.test import TestCase
from todo_app.models import TodoItem, Tag
from todo_app.serializers import TodoItemSerializer, TagSerializer
from django.utils import timezone
from django.utils.timezone import localtime


class TagSerializerTest(TestCase):
    def test_tag_serializer(self):
        tag = Tag.objects.create(name="Important")
        serializer = TagSerializer(tag)
        expected_data = {
            "id": tag.id,
            "name": "Important",
        }
        self.assertEqual(serializer.data, expected_data)


class TodoItemSerializerTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Urgent")
        self.tag2 = Tag.objects.create(name="Home")

    def test_todo_item_serializer(self):
        todo = TodoItem.objects.create(
            title="Buy groceries",
            description="Milk, Bread, Eggs",
            due_date=timezone.now() + timezone.timedelta(days=2),
            status="OPEN",
        )
        todo.tags.set([self.tag1, self.tag2])
        serializer = TodoItemSerializer(todo)

        expected_data = {
            "id": todo.id,
            "timestamp": localtime(todo.timestamp).isoformat(),
            "title": "Buy groceries",
            "description": "Milk, Bread, Eggs",
            "due_date": localtime(todo.due_date).isoformat(),
            "status": "OPEN",
            "tags": [
                {"id": self.tag1.id, "name": "Urgent"},
                {"id": self.tag2.id, "name": "Home"},
            ],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_todo_item_serializer_validation(self):
        data = {
            "title": "",
            "description": "",
            "status": "INVALID_STATUS",
            "tags": [{"name": "Work"}],
        }
        serializer = TodoItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("description", serializer.errors)
        self.assertIn("status", serializer.errors)
        self.assertIn("This field may not be blank.", serializer.errors["title"])
        self.assertIn("This field may not be blank.", serializer.errors["description"])
        self.assertIn(
            '"INVALID_STATUS" is not a valid choice.', serializer.errors["status"]
        )

    def test_validate_tags_with_duplicates(self):
        data = {
            "title": "Duplicate Tags",
            "description": "Testing duplicate tags.",
            "status": "OPEN",
            "tags": [{"name": "Work"}, {"name": "Work"}],
        }
        serializer = TodoItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("tags", serializer.errors)
        self.assertIn(
            "Duplicate tags are not allowed for a single TodoItem.",
            serializer.errors["tags"],
        )

    def test_create_todo_item_with_tags(self):
        data = {
            "title": "Test Create",
            "description": "Testing create method.",
            "due_date": timezone.now() + timezone.timedelta(days=1),
            "status": "OPEN",
            "tags": [{"name": "Tag1"}, {"name": "Tag2"}],
        }
        serializer = TodoItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        todo_item = serializer.save()

        self.assertEqual(todo_item.tags.count(), 2)

    def test_update_todo_item_with_tags(self):
        todo = TodoItem.objects.create(
            title="Initial Title",
            description="Initial description.",
            due_date=timezone.now() + timezone.timedelta(days=1),
            status="OPEN",
        )
        todo.tags.add(self.tag1)

        data = {
            "title": "Updated Title",
            "description": "Updated description.",
            "due_date": timezone.now() + timezone.timedelta(days=2),
            "status": "WORKING",
            "tags": [{"name": "Updated Tag"}, {"name": "Home"}],
        }
        serializer = TodoItemSerializer(todo, data=data)
        self.assertTrue(serializer.is_valid())
        updated_todo = serializer.save()

        self.assertEqual(updated_todo.tags.count(), 2)

    def test_create_todo_item_without_tags(self):
        data = {
            "title": "No Tags",
            "description": "This TodoItem has no tags.",
            "due_date": timezone.now() + timezone.timedelta(days=1),
            "status": "OPEN",
        }
        serializer = TodoItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        todo_item = serializer.save()

        self.assertEqual(todo_item.tags.count(), 0)

    def test_validate_due_date_with_past_date(self):
        """Test that the serializer raises a
        ValidationError for past due_date."""
        data = {
            "title": "Past Due Date",
            "description": "This task has a past due_date.",
            "due_date": timezone.now() - timezone.timedelta(days=1),  # Past date
            "status": "OPEN",
            "tags": [{"name": "Work"}],
        }
        serializer = TodoItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("due_date", serializer.errors)
        self.assertIn("Due date cannot be in the past.", serializer.errors["due_date"])
