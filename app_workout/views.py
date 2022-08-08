from rest_framework import viewsets

from app_workout.models import Workout, Part
from app_workout.serializers import WorkoutInfoSerializer, WorkoutCreateUpdateSerializer, WorkoutInfoWithPartSerializer


class WorkoutViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.request.GET.get("part"):
            return Part.objects.get(name=self.request.GET["part"].strip()).workout_set.all()
        return Workout.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return WorkoutInfoSerializer
        elif self.action == "create":
            return WorkoutCreateUpdateSerializer


class WorkoutDetailViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Workout.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorkoutInfoWithPartSerializer
        if self.action == "partial_update":
            return WorkoutCreateUpdateSerializer
