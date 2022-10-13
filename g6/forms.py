from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Patient

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    gender = forms.ChoiceField(choices=[('Male','Male'), ('Female', 'Female')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1', 'password2',]