from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')
