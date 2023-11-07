from django import forms
from .models import CreditCard, Account

class CreditCardForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.none())
    
    class Meta:
        model = CreditCard
        fields = ['alias', 'account']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(client=user)
