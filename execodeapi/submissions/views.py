# submissions/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from submissions.models import Submission
from problems.models import Problem, TestCase
from submissions.serializers import SubmissionSerializer
from django.shortcuts import get_object_or_404

# Dummy judge function (you’ll replace with real execution logic later)
def judge_submission(code, language, test_cases):
    # Simulate checking all test cases
    for tc in test_cases:
        if "fail" in code:  # Dummy condition
            return "Wrong Answer", 0.2, 15.0
    return "Accepted", 0.1, 12.0

class SubmitSolutionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        problem = get_object_or_404(Problem, pk=id)
        code = request.data.get('code')
        language = request.data.get('language')

        if not code or not language:
            return Response({'detail': 'Code and language are required.'}, status=400)

        submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            language=language
        )

        # Simulate judgment
        test_cases = TestCase.objects.filter(problem=problem, is_sample=False)
        status_result, runtime, memory = judge_submission(code, language, test_cases)

        submission.status = status_result
        submission.runtime = runtime
        submission.memory_usage = memory
        submission.save()

        serializer = SubmissionSerializer(submission)
        return Response(serializer.data)

class MySubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).order_by('-submitted_at')

class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProblemSubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Submission.objects.filter(problem__id=self.kwargs['id']).order_by('-submitted_at')
