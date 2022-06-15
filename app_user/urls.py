from django.urls import path

from app_user import views


def get_users():
    return {
        'get': 'list',
        'post': 'create',
    }


app_name = "app_user"
urlpatterns = [
    path("", views.UserCreateListViewSet.as_view(get_users()))
]
