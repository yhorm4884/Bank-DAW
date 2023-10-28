# forms.py
from django import forms
from .models import CreditCard

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_code', 'alias', 'pin', 'status', 'user']
