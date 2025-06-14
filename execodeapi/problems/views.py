# problems/views.py
from rest_framework import generics, permissions, filters
from .models import Problem, TestCase
from .serializers import ProblemSerializer, TestCaseSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

class ProblemTestCaseListView(generics.ListAPIView):
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        problem_id = self.kwargs['problem_id']
        queryset = TestCase.objects.filter(problem__id=problem_id)
        show_samples_only = self.request.query_params.get('samples_only')
        if show_samples_only == 'true':
            queryset = queryset.filter(is_sample=True)
        return queryset

class TestCaseCreateView(generics.CreateAPIView):
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionError("Only admins can add test cases.")
        serializer.save()