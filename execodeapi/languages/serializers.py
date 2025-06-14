# submissions/serializers.py
from .models import Language
from rest_framework import serializers

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'slug', 'version', 'is_active']
        read_only_fields = ['id']
