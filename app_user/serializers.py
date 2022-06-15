from rest_framework import serializers

from app_user.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "name"]

    def create(self, validated_data):
        instance = User()
        validated_data["password"] = validated_data["password1"]
        del validated_data["password1"]
        del validated_data["password2"]

        for key, value in validated_data.items():
            setattr(instance, key, value) if key != "password" else instance.set_password(value)
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "created_at"]
