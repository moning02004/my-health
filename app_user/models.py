from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


def user_image_path(instance, filename):
    return f'{instance.user_id}_{instance.user.username}/images/{filename}'


class UserRole(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.code}: {self.description}"


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    follow = models.ManyToManyField("self",
                                    through="FollowUser",
                                    symmetrical=False,
                                    through_fields=("user", "follow_user"))

    def __str__(self):
        return f"{self.name}: {self.created_at}"


class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    birth_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}: {self.sex}"


class ProfileImage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.ImageField(upload_to=user_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name}"


class FollowUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="following")
    follow_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="follower")
    created_at = models.DateTimeField(auto_now_add=True)


class Growth(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} [{self.height} / {self.weight}]"
