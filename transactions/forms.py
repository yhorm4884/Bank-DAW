from django import forms
from transactions.models import Transaction


class PaymentForm(forms.Form):
    business = forms.CharField()
    ccc = forms.CharField()
    pin = forms.CharField(widget=forms.PasswordInput)
    amount = forms.DecimalField()

class TransferForm(forms.Form):
    sender = forms.CharField()
    cac = forms.CharField()
    concept = forms.CharField()
    amount = forms.DecimalField()