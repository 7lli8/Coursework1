from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate


from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["email", "name"]
        labels = {
            "name": "Имя"
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["email", "password", "name", "is_active", "is_staff"]


class UserSignInForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        user = authenticate(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        if not user:
            raise forms.ValidationError("Неверный Email или пароль")

        return self.cleaned_data

    def save(self):
        user = authenticate(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        print(user)
        if not user:
            raise forms.ValidationError("Неверный Email или пароль")

        return user
