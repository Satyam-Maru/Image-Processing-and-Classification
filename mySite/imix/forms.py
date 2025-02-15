from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUser(UserCreationForm):
    email = forms.EmailField(required=True)  # Ensure email is required

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']