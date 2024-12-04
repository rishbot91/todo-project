from django.shortcuts import render
from rest_framework import generics, permissions, authentication
from .models import TodoItem
from .serializers import TodoItemSerializer
from django.http import HttpResponse

# Create your views here.
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'todos': reverse('todo-list-create', request=request, format=format),
#     })

def home(request):
    return render(request, 'home.html')

class TodoItemListCreateView(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class TodoItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]