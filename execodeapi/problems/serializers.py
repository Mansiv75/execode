# problems/serializers.py
from rest_framework import serializers
from .models import Problem, TestCase

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'acceptance_rate']

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'problem', 'input_data', 'expected_output', 'is_sample']
        read_only_fields = ['id']