from django import forms
from .models import Account

class AccountRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Current Password')

    class Meta:
        model = Account
        fields = ['alias', 'password']


    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if Account.objects.filter(alias=alias).exists():
            raise forms.ValidationError('Este alias ya está en uso.')
        return alias

class AccountEditForm(forms.ModelForm):
    alias = forms.CharField(max_length=255)
    class Meta:
        model = Account
        fields = ['alias']
    def clean_alias(self):
        alias = self.cleaned_data['alias']
        if Account.objects.filter(alias=alias).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Este alias ya está en uso.')
        return alias
        
class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount',
        min_value=0.01,
        widget=forms.NumberInput(attrs={'step': '0.01'}),
    )