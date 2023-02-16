from django.contrib import admin

from apps.account.models import User, FollowUser

admin.site.register(User)
admin.site.register(FollowUser)