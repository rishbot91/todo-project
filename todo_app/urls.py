from django.urls import path
from .views import TodoItemListCreateView, TodoItemDetailView

urlpatterns = [
    path('todos/', TodoItemListCreateView.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', TodoItemDetailView.as_view(), name='todo-detail'),
]
