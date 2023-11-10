from django import forms

from .models import Transfer


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['sender', 'cac', 'concept', 'amount']
