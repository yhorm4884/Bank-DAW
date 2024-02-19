from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Client, Account,CreditCard
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Usuario

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = super().clean()
        user = authenticate(self.request, username=cd['username'], password=cd['password'])
        if user is None:
            raise forms.ValidationError('Invalid login')
        return cd



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password', 'required': 'required'})
    )
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password', 'required': 'required'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'required': 'required'}),
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name' , 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Enter last name' , 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control' , 'placeholder': 'Enter email' , 'required': 'required'}),

        }

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return data

# Clientes
    
class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['photo']


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['photo']

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
        max_value=1000000,  
        widget=forms.NumberInput(attrs={'step': '0.01', 'max': '1000000'}),  
        error_messages={'max_value': 'El cantidad no puede superar 1 millón de euros'},
    )

# Tarjetas de crédito.
    
class CreditCardFormWithoutAccount(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['alias']

class CreditCardForm(forms.ModelForm):
    account = forms.ModelChoiceField(queryset=Account.objects.none())
    
    class Meta:
        model = CreditCard
        fields = ['alias', 'account']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(client=user)
