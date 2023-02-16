import logging

from django.db import transaction
from rest_framework import serializers

from apps.workout.models import Workout, Part


class WorkoutInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["name", "description", "status"]


class WorkoutInfoWithPartSerializer(serializers.ModelSerializer):
    effective_part = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Workout
        fields = ["name", "description", "effective_part"]


class WorkoutCreateUpdateSerializer(serializers.ModelSerializer):
    part_id = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=True)
    representation_id = serializers.IntegerField(required=False)

    class Meta:
        model = Workout
        fields = ["name", "description", "part_id", "representation_id", "status"]

    def create(self, validated_data):
        with transaction.atomic():
            instance = Workout()
            for key, value in validated_data.items():
                if key in ["name", "description", "representation_id"]:
                    setattr(instance, key, value)
                if key == "status":
                    setattr(instance, key, str(value)[:3].upper())
            instance.registered_by = self.context["request"].user
            instance.save()

            for _id in validated_data["part_id"]:
                instance.effective_part.add(Part.objects.get(pk=_id))
            return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            for key, value in validated_data.items():
                if key in ["name", "description", "representation_id"]:
                    setattr(instance, key, value)
                if key == "status":
                    setattr(instance, key, str(value)[:3].upper())
            instance.save()

            for _id in validated_data.get("part_id", []):
                instance.effective_part.add(Part.objects.get(pk=_id))
            return instance
