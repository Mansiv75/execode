# problems/views.py
from rest_framework import generics, permissions, filters
from .models import Problem
from .serializers import ProblemSerializer

class ProblemListCreateView(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'difficulty']

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionError("Only admins can create problems.")
        serializer.save()

class ProblemRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionError("Only admins can update problems.")
        serializer.save()
