from rest_framework import serializers
from .models import CodeExecution

class CodeExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeExecution
        fields = '__all__'
        read_only_fields = ['id', 'user', 'output', 'error_message', 'status', 
                           'execution_time', 'memory_usage', 'created_at']

class RunCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    language = serializers.IntegerField()  # Language ID
    input_data = serializers.CharField(required=False, default='')
    problem_id = serializers.IntegerField(required=False)