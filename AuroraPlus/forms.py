from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class OptionsForm(forms.Form):
    active_monitoring = forms.BooleanField(required=False)
    opacity = forms.BooleanField(required=False)
