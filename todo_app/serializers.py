from rest_framework import serializers
from .models import TodoItem, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TodoItemSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = TodoItem
        fields = ['id', 'timestamp', 'title', 'description', 'due_date', 'tags', 'status']
        read_only_fields = ['timestamp']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        todo_item = TodoItem.objects.create(**validated_data)
        for tag_data in tags_data:
            tag_name = tag_data['name']
            tag, created = Tag.objects.get_or_create(name=tag_name)
            todo_item.tags.add(tag)
        return todo_item

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag_name = tag_data['name']
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        return instance
