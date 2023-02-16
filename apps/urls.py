from django.urls import path, include

list_actions = {
    'get': 'list',
    'post': 'create',
}

detail_actions = {
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
}

urlpatterns = [
    path("/users", include("apps.account.urls")),
    path("/workout", include("apps.workout.urls")),
]