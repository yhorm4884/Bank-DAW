from django import forms
from transactions.models import Transaction


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['agent', 'concept', 'amount', 'kind']
