from django.urls import path

from app_user import views


def route_users():
    return {
        'get': 'list',
        'post': 'create',
    }


def route_user():
    return {
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    }


app_name = "app_user"
urlpatterns = [
    path("", views.UserCreateListViewSet.as_view(route_users())),
    path("/<int:pk>", views.UserDetailViewSet.as_view(route_user())),
]
