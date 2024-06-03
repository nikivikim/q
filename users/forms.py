from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import forms, inlineformset_factory
from django import forms
from .models import Indicator, Balance, IndicatorValue, ActivityType
from users.models import Indicator, Balance, IndicatorValue

User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        labels = {
            'username':'Имя пользователя (логин)',
            'first_name': 'Имя',
            'password1': 'Имя пользователя (логин)',
            'first_name': 'Имя',
        }
class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['company_name', 'activity_type', 'date']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class IndicatorValueForm(forms.ModelForm):
    class Meta:
        model = IndicatorValue
        fields = ['value', 'value2', 'value3']
        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'value2': forms.NumberInput(attrs={'class': 'form-control'}),
            'value3': forms.NumberInput(attrs={'class': 'form-control'}),
        }