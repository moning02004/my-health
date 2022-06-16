from rest_framework import serializers

from app_user.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "created_at"]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "name"]

    def validate(self, attrs):
        if not self.partial:
            if not all([attrs.get(x) for x in self.Meta.fields]):
                raise serializers.ValidationError('입력하신 내용을 확인해주십시오.')
        return super().validate(attrs)

    def create(self, validated_data):
        instance = User()
        for key, value in validated_data.items():
            setattr(instance, key, value) if key != "password" else instance.set_password(value)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) if key != "password" else instance.set_password(value)
        instance.save()
        return instance
