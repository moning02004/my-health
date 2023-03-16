from django.contrib import admin

from apps.account.models import Account, AccountFollow

admin.site.register(Account)
admin.site.register(AccountFollow)