from django.contrib import admin
from .models import TodoItem, Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    list_display = ('title', 'status', 'due_date', 'timestamp')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status')
        }),
        ('Optional Information', {
            'fields': ('due_date', 'tags')
        }),
        ('Read-Only Fields', {
            'fields': ('timestamp',)
        }),
    )
