from django.contrib import admin
from .models import Client, Account, CreditCard

class CreditCardInline(admin.TabularInline):
    model = CreditCard
    extra = 1

class AccountInline(admin.TabularInline):
    model = Account
    extra = 1
    inlines = [CreditCardInline]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')
    search_fields = ('user__username', 'user__email')
    inlines = [AccountInline]

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'alias', 'client', 'balance', 'status')
    search_fields = ('code', 'alias', 'client__user__username')
    list_filter = ('status',)
    inlines = [CreditCardInline]

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('card_code', 'alias', 'status', 'account')
    search_fields = ('card_code', 'alias', 'account__code')
    list_filter = ('status',)
