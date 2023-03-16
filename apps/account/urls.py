from django.urls import path

from apps.account import views
from my_health.urls import list_actions, detail_actions

app_name = "account"
urlpatterns = [
    path("", views.AccountCreateListViewSet.as_view(list_actions), name="list"),
    path("/@<str:username>", views.AccountDetailViewSet.as_view(detail_actions), name="single"),
    path("/@<str:username>/follower", views.AccountFollowerAPI.as_view(), name="follower"),
    path("/@<str:username>/following", views.AccountFollowingAPI.as_view({
        "get": "list",
        "post": "partial_update"
    }), name="following"),
]
