from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.account.models import Account


class AccountInfoSerializer(serializers.ModelSerializer):
    following_count = serializers.IntegerField()
    follower_count = serializers.IntegerField()

    class Meta:
        model = Account
        fields = ["id", "username", "name", "description", "following_count", "follower_count"]


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "password", "name"]
        read_only_fields = ["id"]
        extra_kwargs = {
            'password': {'write_only': True},
            'name': {'write_only': True},
        }

    def create(self, validated_data):
        instance = Account()
        password = validated_data.pop("password")
        instance.set_password(password)
        [setattr(instance, key, value) for key, value in validated_data.items()]
        instance.save()
        return instance


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "password", "name"]
        read_only_fields = ["id", "username"]
        extra_kwargs = {
            'password': {'write_only': True},
            'name': {'write_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.get("password") and validated_data.pop("password")
        do_update = False
        if password:
            do_update = True
            instance.set_password(password)
        [setattr(instance, key, value) for key, value in validated_data.items()]
        (do_update or validated_data) and instance.save()
        return instance


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["username", "name"]


class FollowUpdateSerializer(serializers.ModelSerializer):
    follow = None
    follow_user = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ["follow_user"]

    def validate(self, attrs):
        try:
            self.follow = Account.objects.get(username=attrs["follow_user"])
            if self.follow == self.context["request"].user:
                raise ValidationError({"detail": "자기자신을 팔로우할 수 없습니다."}, code="invalid")
        except Account.DoesNotExist:
            raise ValidationError({"detail": "해당 사용자가 없습니다."}, code="invalid")
        return attrs

    def update(self, instance: Account, validated_data):
        if not instance.follow.filter(follow=self.follow).exists():
            instance.follow.add(self.follow)
        else:
            instance.follow.remove(self.follow)
        return instance
