from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from submissions.models import Submission  # Assuming your Submission model is there
from django.db.models import Count

User = get_user_model()

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicUserView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        solved = Submission.objects.filter(user=user, status='Accepted').values('problem').distinct().count()
        attempted = Submission.objects.filter(user=user).values('problem').distinct().count()

        # Optional: calculate streaks later
        return Response({
            'solved_problems': solved,
            'attempted_problems': attempted,
            'streak': 0  # Implement streak logic later
        })
