from django.urls import path
from .views import RunCodeView, ExecutionHistoryView, ExecutionDetailView

urlpatterns = [
    path('run/', RunCodeView.as_view(), name='run-code'),
    path('history/', ExecutionHistoryView.as_view(), name='execution-history'),
    path('history/<int:pk>/', ExecutionDetailView.as_view(), name='execution-detail'),
]