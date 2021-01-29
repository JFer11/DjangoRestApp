from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class NameForm(forms.Form):
    name = forms.CharField(label='First name', max_length=100)
    birth = forms.DateTimeField()
    created = forms.DateTimeField()
    updated = forms.DateTimeField()
    gender = forms.BooleanField(required=False)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email", "password1", "password2",)
        # field_classes = {'username': UsernameField}


class LoginUserForm(AuthenticationForm):
    pass
