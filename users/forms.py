from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#Изменить вход, так как имя пользователя не должно быть
class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254)
    password = forms.PasswordInput()
