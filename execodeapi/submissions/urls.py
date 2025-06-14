# submissions/urls.py
from django.urls import path
from .views import SubmitSolutionView, MySubmissionsView, SubmissionDetailView, ProblemSubmissionsView

urlpatterns = [
    path('problems/<int:id>/submit/', SubmitSolutionView.as_view(), name='submit-solution'),
    path('submissions/', MySubmissionsView.as_view(), name='my-submissions'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('problems/<int:id>/submissions/', ProblemSubmissionsView.as_view(), name='problem-submissions'),
]
