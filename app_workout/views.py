from rest_framework import viewsets

from app_workout.models import Workout
from app_workout.serializers import WorkoutInfoSerializer, WorkoutCreateUpdateSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return WorkoutInfoSerializer
        elif self.action == "create":
            return WorkoutCreateUpdateSerializer
