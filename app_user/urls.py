from django.urls import path

from app_user import views

list_actions = {
    'get': 'list',
    'post': 'create',
}

detail_actions = {
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
}

app_name = "app_user"
urlpatterns = [
    path("", views.UserCreateListViewSet.as_view(list_actions)),
    path("/<int:pk>", views.UserDetailViewSet.as_view(detail_actions)),
    path("/<int:pk>/followers", views.FollowCreateListViewSet.as_view(detail_actions)),
]
