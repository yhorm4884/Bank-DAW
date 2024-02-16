from django import forms
from transactions.models import Transaction


class PaymentForm(forms.Form):
    business = forms.CharField(required=True)
    ccc = forms.CharField(required=True)
    pin = forms.CharField(widget=forms.PasswordInput, required=True)
    amount = forms.DecimalField(required=True)

class TransferForm(forms.Form):
    sender = forms.CharField(required=True)
    cac = forms.CharField(required=True)
    concept = forms.CharField(required=True)
    amount = forms.DecimalField(required=True)

