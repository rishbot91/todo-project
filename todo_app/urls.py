from django.urls import path
from .views import TodoItemListCreateView, TodoItemDetailView
from . import views
# from django.views.generic import RedirectView

urlpatterns = [
    # path('', RedirectView.as_view(url='todos/', permanent=False)),
    # path("", views.index, name="index"),
    path('todos/', TodoItemListCreateView.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', TodoItemDetailView.as_view(), name='todo-detail'),
]