from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    list_display = ('username', 'status', 'photo')
    list_filter = ('status',)
