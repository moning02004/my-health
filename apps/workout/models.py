from django.contrib.auth import get_user_model
from django.db import models


# 운동 부위
class Part(models.Model):
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=300, null=True)

    class Meta:
        db_table = "part"


# 운동 종목
class Workout(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                                      related_name="register_workout")
    effective_part = models.ManyToManyField(Part)

    class Meta:
        db_table = "workout"
