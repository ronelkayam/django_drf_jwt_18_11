from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .models import Workout
from .serializers import WorkoutSerializer, RegisterSerializer
from .mongo_client import get_audit_collection


# Create your views here.
class RegisterView(generics.CreateAPIView):
    """
    end point for POST /api/register/
    open to everybody for user could register and get token (AllowAny)
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class WorkoutListCreateView(generics.ListCreateAPIView):
    """
    all from /api/workouts
    GET -> get all workouts for connection user only
    POST-> create new workout (SQL SERVER) -> SIGNAL report to MongoDB
    """

    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]  # request JWT valid token

    def get_queryset(self):
        # filter that all user see only his workouts only
        return Workout.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # מצמיד אוטומטית את המשתמש לאימון החדש מתוך הJWT TOken
        serializer.save(user=self.request.user)


class AuditLogView(APIView):
    """
    GET-> /api/logs-> get all history actions from mongoDB
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        collection = get_audit_collection()
        logs = list(
            collection.find(
                {
                    "username": request.user.username},
                {"_id": 0}
            ).sort("timestamp", -1)
        )
        return Response({
            "source_db":"MongoDB",
            "user": request.user.username,
            "total_events": len(logs),
            "logs": logs
        },status=status.HTTP_200_OK)