from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.account.models import User
from apps.account.serializers import UserInfoSerializer, UserCreateUpdateSerializer, UserFollowSerializer, \
    UserFollowCreateUpdateSerializer


class UserCreateListViewSet(ModelViewSet):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UserInfoSerializer
        elif self.action == "create":
            return UserCreateUpdateSerializer
        return ModelSerializer

    def check_permissions(self, request):
        if self.action == "create":
            return [AllowAny]
        return [IsAuthenticated]


class UserDetailViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserInfoSerializer
        if self.action == "partial_update":
            return UserCreateUpdateSerializer
        if self.action == "destroy":
            return ModelSerializer


class FollowListAPI(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowSerializer


class FollowOnOffAPI(CreateAPIView, UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowCreateUpdateSerializer
