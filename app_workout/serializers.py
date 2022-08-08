from django.db import transaction
from rest_framework import serializers

from app_workout.models import Workout, Part


class PartInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ["name"]


class WorkoutInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["name", "description", "status"]


class WorkoutInfoWithPartSerializer(serializers.ModelSerializer):
    effective_part = PartInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ["name", "description", "effective_part"]


class WorkoutCreateUpdateSerializer(serializers.ModelSerializer):
    part_id = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    representation_id = serializers.IntegerField(required=False)

    class Meta:
        model = Workout
        fields = ["name", "description", "part_id", "representation_id"]

    def create(self, validated_data):
        try:
            with transaction.atomic():
                instance = Workout()
                for key, value in validated_data.items():
                    if key in ["name", "description", "representation_id"]:
                        setattr(instance, key, value)
                instance.registered_by = self.context["request"].user
                instance.save()

                for _id in validated_data["part_id"]:
                    instance.effective_part.add(Part.objects.get(pk=_id))
                return instance
        except Exception as e:
            raise serializers.ValidationError('입력하신 내용을 확인해주십시오.')
