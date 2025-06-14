# problems/serializers.py
from rest_framework import serializers
from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'acceptance_rate']
