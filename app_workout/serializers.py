from rest_framework import serializers

from app_workout.models import Workout, Part


class WorkoutInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["name", "description", "status"]


class WorkoutCreateUpdateSerializer(serializers.ModelSerializer):
    part_id = serializers.IntegerField(write_only=True)
    representation_id = serializers.IntegerField(required=False)

    class Meta:
        model = Workout
        fields = ["name", "description", "part_id", "representation_id"]

    def create(self, validated_data):
        instance = Workout()
        for key, value in validated_data.items():
            if key in ["name", "description", "representation_id"]:
                setattr(instance, key, value)
        instance.registered_by = self.context["request"].user
        instance.save()

        instance.effective_part.add(Part.objects.get(pk=validated_data["part_id"]))
        return instance
