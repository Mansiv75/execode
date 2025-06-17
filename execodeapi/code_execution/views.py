from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CodeExecution
from .serializers import CodeExecutionSerializer, RunCodeSerializer
from .executor import CodeExecutor
from languages.models import Language
from problems.models import Problem

class RunCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = RunCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        try:
            language = Language.objects.get(pk=data['language'])
        except Language.DoesNotExist:
            return Response({'error': 'Invalid language'}, status=status.HTTP_400_BAD_REQUEST)
        
        problem = None
        if data.get('problem_id'):
            try:
                problem = Problem.objects.get(pk=data['problem_id'])
            except Problem.DoesNotExist:
                return Response({'error': 'Invalid problem'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create execution record
        execution = CodeExecution.objects.create(
            user=request.user,
            problem=problem,
            code=data['code'],
            language=language,
            input_data=data['input_data']
        )
        
        # Execute code
        executor = CodeExecutor(
            code=data['code'],
            language_slug=language.slug,
            input_data=data['input_data']
        )
        
        result = executor.execute()
        
        # Update execution record
        execution.status = result['status']
        execution.output = result['output']
        execution.error_message = result['error']
        execution.execution_time = result['execution_time']
        execution.memory_usage = result['memory_usage']
        execution.save()
        
        return Response(CodeExecutionSerializer(execution).data)

class ExecutionHistoryView(generics.ListAPIView):
    serializer_class = CodeExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CodeExecution.objects.filter(user=self.request.user).order_by('-created_at')

class ExecutionDetailView(generics.RetrieveAPIView):
    serializer_class = CodeExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CodeExecution.objects.filter(user=self.request.user)