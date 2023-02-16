from django.contrib.auth import get_user_model
from django.db import models

from apps.workout.models import Workout


class History(models.Model):
    weight = models.FloatField()
    set_count = models.PositiveSmallIntegerField(default=1)
    memo = models.CharField(max_length=300)
    executed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.executed_at}: {self.workout.name}"
