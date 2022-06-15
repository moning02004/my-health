from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from app_user.models import User
from app_user.serializers import UserListSerializer, UserCreateSerializer


class UserCreateListViewSet(ModelViewSet):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        elif self.action == "create":
            return UserCreateSerializer
        return ModelSerializer

    # def create(self, request, *args, **kwargs):
    #     super().create(request, *args, **kwargs)