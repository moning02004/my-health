from django.db.models import Count, Q, F
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from apps.account.models import Account
from apps.account.serializers import AccountInfoSerializer, AccountCreateSerializer, AccountUpdateSerializer, \
    FollowerSerializer, FollowUpdateSerializer


class AccountCreateListViewSet(ModelViewSet):
    def get_queryset(self):
        return Account.objects.annotate(following_count=Count("following"),
                                        follower_count=Count("follower")).all()

    def get_serializer_class(self):
        if self.action == "list":
            return AccountInfoSerializer
        if self.action == "create":
            return AccountCreateSerializer

    def check_permissions(self, request):
        if self.action == "create":
            return [AllowAny]
        return [IsAuthenticated]


class AccountDetailViewSet(ModelViewSet):
    lookup_field = "username"

    def get_queryset(self):
        return Account.objects.annotate(following_count=Count("following"),
                                        follower_count=Count("follower")).all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AccountInfoSerializer
        if self.action == "partial_update":
            return AccountUpdateSerializer
        if self.action == "destroy":
            return ModelSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class AccountFollowerAPI(ListAPIView):
    lookup_field = "username"
    serializer_class = FollowerSerializer

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = Account.objects.filter(username=username)
        if queryset.exists():
            account = queryset.first().follower.annotate(username=F("account__username"), name=F("account__name")).all()
            return account
        return Account.objects.none()


class AccountFollowingAPI(ModelViewSet):
    lookup_field = "username"

    def get_queryset(self):
        if self.action == "partial_update":
            return Account.objects.all()

        username = self.kwargs["username"]
        queryset = Account.objects.filter(username=username)
        if queryset.exists():
            queryset = queryset.first().following.annotate(username=F("follow__username"),
                                                           name=F("follow__name")).all()
            keyword = self.request.GET.get("keyword")
            if keyword:
                queryset = queryset.filter(Q(username__icontains=keyword) | Q(name__contains=keyword))
            return queryset
        return Account.objects.none()

    def get_serializer_class(self):
        if self.action == "list":
            return FollowerSerializer
        if self.action == "partial_update":
            return FollowUpdateSerializer
