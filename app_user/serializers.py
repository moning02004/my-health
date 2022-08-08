import logging

from rest_framework import serializers

from app_user.models import User, FollowUser


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


class FollowingInfoSerializer(serializers.ModelSerializer):
    follow_user = UserInfoSerializer()

    class Meta:
        model = FollowUser
        fields = ["follow_user", "created_at"]


class FollowerInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    class Meta:
        model = FollowUser
        fields = ["user", "created_at"]


class UserFollowSerializer(serializers.ModelSerializer):
    following = FollowingInfoSerializer(many=True)
    follower = FollowerInfoSerializer(many=True)

    class Meta:
        model = User
        fields = ["username", "following", "follower"]


class UserFollowCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []

    def validate(self, attrs):
        try:
            self.context["view"].kwargs
        except Exception as e:
            logging.error(type(e))
            raise serializers.ValidationError('입력하신 내용을 확인해주십시오.')
        return attrs

    def create(self, validated_data):
        current_user = self.context["request"].user
        follow_user_id = self.context["view"].kwargs["pk"]
        if User.objects.filter(pk=follow_user_id).exists():
            current_user.follow.add(User.objects.get(pk=follow_user_id))
        return validated_data

    def update(self, instance, validated_data):
        current_user = self.context["request"].user
        current_user.follow.remove(instance)
        return validated_data
