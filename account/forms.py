from django import forms
from django.core.validators import FileExtensionValidator
from .models import Account

class AccountRegistrationForm(forms.ModelForm):
    photo = forms.ImageField(validators=[FileExtensionValidator(['jpg', 'png'])])
    alias = forms.CharField(max_length=255)

    class Meta:
        model = Account
        fields = ['alias','photo']

class AccountEditForm(forms.ModelForm):
    photo = forms.ImageField(validators=[FileExtensionValidator(['jpg', 'png'])])
    alias = forms.CharField(max_length=255)
    class Meta:
        model = Account
        fields = ['alias','photo']
        
