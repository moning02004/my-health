from django.urls import path

from app_user import views
from my_health.urls import list_actions, detail_actions

app_name = "app_user"
urlpatterns = [
    path("", views.UserCreateListViewSet.as_view(list_actions)),
    path("/<int:pk>", views.UserDetailViewSet.as_view(detail_actions)),
    path("/<int:pk>/followers", views.FollowListAPI.as_view()),
    path("/<int:pk>/follow", views.FollowOnOffAPI.as_view()),
    path("/<int:pk>/unfollow", views.FollowOnOffAPI.as_view()),
]
