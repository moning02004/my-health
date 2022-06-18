from django.contrib import admin

from app_user.models import User, FollowUser

admin.site.register(User)
admin.site.register(FollowUser)