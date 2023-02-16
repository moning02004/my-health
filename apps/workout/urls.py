from django.urls import path

from apps.workout import views
from my_health.urls import list_actions, detail_actions

urlpatterns = [
    path("", views.WorkoutViewSet.as_view(list_actions)),
    path("<int:pk>", views.WorkoutDetailViewSet.as_view(detail_actions))
]