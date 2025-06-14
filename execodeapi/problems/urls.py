# problems/urls.py
from django.urls import path
from .views import ProblemListCreateView, ProblemRetrieveUpdateView, ProblemTestCaseListView, TestCaseCreateView

urlpatterns = [
    path('problems/', ProblemListCreateView.as_view(), name='problem-list-create'),
    path('problems/<int:pk>/', ProblemRetrieveUpdateView.as_view(), name='problem-detail-update'),
    path('problems/<int:problem_id>/test-cases/', ProblemTestCaseListView.as_view(), name='problem-test-cases'),
    path('test-cases/add/', TestCaseCreateView.as_view(), name='add-test-case'),
]
