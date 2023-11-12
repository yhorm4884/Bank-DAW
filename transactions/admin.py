from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('kind', 'agent', 'amount', 'timestamp')
    list_filter = ('kind', 'agent')
    search_fields = ('concept', 'amount', 'timestamp')