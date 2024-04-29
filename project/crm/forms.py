from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

# - Create/Register a user (Model Form)
class CreateUserForm(UserCreationForm):

    first_name = forms.CharField(widget=TextInput())
    last_name = forms.CharField(widget=TextInput())
    username = forms.CharField(widget=TextInput())
    email = forms.CharField(widget=TextInput())
    password1 = forms.CharField(widget=PasswordInput())
    password2 = forms.CharField(widget=PasswordInput())
    
    class Meta:

        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

# - Authenticate a user (Model Form)
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())