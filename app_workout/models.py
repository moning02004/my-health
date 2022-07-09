from django.contrib.auth import get_user_model
from django.db import models


# 운동 부위
class Part(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


# 운동 종목
class Workout(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    representation = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=3, default="REG")
    registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    effective_part = models.ManyToManyField(Part)

    def __str__(self):
        return self.name


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
