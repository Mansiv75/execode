# submissions/serializers.py
from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['id', 'user', 'status', 'runtime', 'memory_usage', 'submitted_at']
