from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=False)

    def __str__(self):
        return self.name


class TodoItem(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('WORKING', 'Working'),
        ('PENDING REVIEW', 'Pending Review'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='OPEN',
    )

    def clean(self):
        super().clean()
        current_time = timezone.now()
        due_date = self.due_date
        if due_date and due_date < current_time:
            raise ValidationError('Due date cannot be in the past.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls the clean method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
