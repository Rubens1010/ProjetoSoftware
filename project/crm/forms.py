from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django.utils import timezone

from .models import FinancialData


# - Create/Register a user (Model Form)
class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
                "id": "floatingInput",
            }
        )
    )
    last_name = forms.CharField(
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name",
                "id": "floatingInput",
            }
        )
    )
    username = forms.CharField(
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "id": "floatingInput",
            }
        )
    )
    email = forms.CharField(
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "id": "floatingInput",
            }
        )
    )
    password1 = forms.CharField(
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "floatingInput",
            }
        )
    )
    password2 = forms.CharField(
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
                "id": "floatingInput",
            }
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
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "username",
                "id": "floatingInput",
            }
        )
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "floatingInputPassword",
            }
        )
    )


class FinancialDataForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget, initial=timezone.now().date)

    class Meta:
        model = FinancialData
        fields = ["monthly_income", "monthly_expense", "date", "description"]
