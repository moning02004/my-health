from django.urls import path

from app_workout import views
from my_health.urls import list_actions

urlpatterns = [
    path("", views.WorkoutViewSet.as_view(list_actions))
]