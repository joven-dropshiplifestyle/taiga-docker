from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'project_id', 'project_name')
    search_fields = ('username', 'email')
    ordering = ('id',)


admin.site.register(Account, AccountAdmin)
