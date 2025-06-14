# auth_api/urls.py
from django.urls import path
from .views import MeView, PublicUserView, UserStatsView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('<int:id>/', PublicUserView.as_view(), name='public_user'),
    path('me/stats/', UserStatsView.as_view(), name='user_stats'),
]
