from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


def user_image_path(instance, filename):
    return f'{instance.user_id}_{instance.user.username}/images/{filename}'


class Account(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, default="")
    is_deleted = models.BooleanField(default=False)

    follow = models.ManyToManyField("self",
                                    through="AccountFollow",
                                    symmetrical=False,  # add 시 동시 추가 방지
                                    through_fields=("account", "follow"))

    class Meta:
        db_table = "account"


class Profile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female"), ("", "Other")])
    birth_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "profile"


class ProfileAvatar(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="avatars")
    hash_id = models.CharField(max_length=100, unique=True)

    file = models.ImageField(upload_to=user_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "profile_avatar"


class AccountFollow(models.Model):
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="following")
    follow = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="follower")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "account_follow"


class Growth(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="growth_list")
    height = models.FloatField()
    weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "growth"
