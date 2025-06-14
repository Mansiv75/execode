# submissions/urls.py

from django.urls import path
from .views import LanguageListView, LanguageAdminView

urlpatterns = [
    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('admin/languages/', LanguageAdminView.as_view(), name='language-admin'),
]
