from django.contrib.auth import get_user_model
from django.db import models


class Workout(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    representation = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=3, default="REG")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
