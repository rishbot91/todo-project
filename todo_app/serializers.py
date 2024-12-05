from rest_framework import serializers
from .models import TodoItem, Tag
from django.utils import timezone


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']  # Make 'id' read-only
        extra_kwargs = {
            'name': {'validators': []},  # Remove uniqueness validator
        }


class TodoItemSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = TodoItem
        fields = [
            'id',
            'timestamp',
            'title',
            'description',
            'due_date',
            'tags',
            'status',
        ]
        read_only_fields = ['timestamp']

    def validate_tags(self, value):
        """Ensure that no duplicate tags are associated with the TodoItem."""
        tag_names = [tag.get('name') for tag in value]
        if len(tag_names) != len(set(tag_names)):
            raise serializers.ValidationError(
                "Duplicate tags are not allowed for a single TodoItem."
            )
        return value

    def validate_due_date(self, value):
        """Ensure due_date is not in the past."""
        if value and value < timezone.now():
            raise serializers.ValidationError(
                "Due date cannot be in the past."
            )
        return value

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        todo_item = TodoItem.objects.create(**validated_data)
        tag_names = set()
        for tag_data in tags_data:
            tag_name = tag_data['name']
            if tag_name not in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                todo_item.tags.add(tag)
                tag_names.add(tag_name)
        return todo_item

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data:
            instance.tags.clear()
            tag_names = set()
            for tag_data in tags_data:
                tag_name = tag_data['name']
                if tag_name not in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
                    tag_names.add(tag_name)
        return instance
