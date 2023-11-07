from django.contrib import admin

from .models import Account


@admin.register(Account)
class ProfileAdmin(admin.ModelAdmin):
    # Lista de datos a mostrar al administrador al ver los perfiles de usuarios
    list_display = ['code', 'status']

    # Implementados los filtros por los que puede el administrador buscar
    list_filter = ['code', 'status']
