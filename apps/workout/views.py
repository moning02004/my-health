from django.db.models import Q
from rest_framework import viewsets

from apps.workout.models import Workout
from apps.workout.serializers import WorkoutInfoSerializer, WorkoutCreateUpdateSerializer, WorkoutInfoWithPartSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        query = Q(status=self.request.GET.get("status", "PUB"))
        if self.request.GET.get("part"):
            query.add(Q(effective_part__name=self.request.GET["part"]), Q.AND)
        return Workout.objects.prefetch_related("effective_part").filter(query)

    def get_serializer_class(self):
        if self.action == "list":
            return WorkoutInfoSerializer
        elif self.action == "create":
            return WorkoutCreateUpdateSerializer


class WorkoutDetailViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Workout.objects.prefetch_related("effective_part").filter(status=self.request.GET.get("status", "PUB"))

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorkoutInfoWithPartSerializer
        if self.action == "partial_update":
            return WorkoutCreateUpdateSerializer
