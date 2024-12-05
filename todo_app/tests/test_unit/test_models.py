from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from todo_app.models import TodoItem, Tag


class TagModelTest(TestCase):
    def test_tag_creation(self):
        tag = Tag.objects.create(name="Urgent")
        self.assertEqual(tag.name, "Urgent")
        self.assertEqual(str(tag), "Urgent")

    def test_tag_name_uniqueness(self):
        Tag.objects.create(name="Urgent")
        with self.assertRaises(Exception):
            Tag.objects.create(name="Urgent")


class TodoItemModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Work")

    def test_todo_item_creation(self):
        todo = TodoItem.objects.create(
            title="Finish report",
            description="Complete the annual report.",
            due_date=timezone.now() + timezone.timedelta(days=1),
            status="OPEN",
        )
        todo.tags.add(self.tag)
        self.assertEqual(todo.title, "Finish report")
        self.assertEqual(todo.description, "Complete the annual report.")
        self.assertEqual(todo.status, "OPEN")
        self.assertIn(self.tag, todo.tags.all())
        self.assertIsNotNone(todo.timestamp)
        self.assertEqual(str(todo), "Finish report")

    def test_due_date_before_timestamp(self):
        past_due_date = timezone.now() - timezone.timedelta(days=1)
        todo = TodoItem(
            title="Past Task",
            description="This task has a past due date.",
            due_date=past_due_date,
            status="OPEN",
        )
        with self.assertRaises(ValidationError) as context:
            todo.full_clean()
        self.assertIn(
            "Due date cannot be in the past.",
            str(context.exception),
        )

    def test_status_choices(self):
        todo = TodoItem(
            title="Test Status",
            description="Testing status choices.",
            status="INVALID_STATUS",
        )
        with self.assertRaises(ValidationError) as context:
            todo.full_clean()
        self.assertIn(
            "Value 'INVALID_STATUS' is not a valid choice.",
            str(context.exception),
        )
