# submissions/views.py
from rest_framework import generics, permissions
from .models import Language
from .serializers import LanguageSerializer

class LanguageListView(generics.ListAPIView):
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer
    permission_classes = [permissions.AllowAny]

# Optional admin views
class LanguageAdminView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAdminUser]
