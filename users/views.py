from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserCreationForm, UserSignInForm

def signin_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserSignInForm()
    return render(request, "users/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Здесь вы можете выполнить дополнительные действия после успешной регистрации
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def account_view(request):
    return render(request, "users/account.html")


def contacts_view(request):
    return render(request, "users/contacts.html")


def help_view(request):
    return render(request, "users/contacts.html")
