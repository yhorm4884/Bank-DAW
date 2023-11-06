from django import forms
from django.core.validators import FileExtensionValidator
from .models import Account

class AccountForm(forms.ModelForm):
    avatar = forms.ImageField(validators=[FileExtensionValidator(['jpg', 'png'])])
    alias = forms.CharField(max_length=255)

    class Meta:
        model = Account
        fields = ['alias','avatar']

class AccountEditForm(forms.ModelForm):
    avatar = forms.ImageField(validators=[FileExtensionValidator(['jpg', 'png'])])
    alias = forms.CharField(max_length=255)
    class Meta:
        model = Account
        fields = ['alias','avatar']
        
