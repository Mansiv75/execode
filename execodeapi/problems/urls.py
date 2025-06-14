# problems/urls.py
from django.urls import path
from .views import ProblemListCreateView, ProblemRetrieveUpdateView

urlpatterns = [
    path('problems/', ProblemListCreateView.as_view(), name='problem-list-create'),
    path('problems/<int:pk>/', ProblemRetrieveUpdateView.as_view(), name='problem-detail-update'),
]
