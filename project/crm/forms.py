from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


# - Create/Register a user (Model Form)
class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        widget=TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )
    username = forms.CharField(
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    email = forms.CharField(
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password1 = forms.CharField(
        widget=PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
        )
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


# - Authenticate a user (Model Form)
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={"class": "form-control", "placeholder": "username"})
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={"class": "form-control", "placeholder": "password"})
    )
