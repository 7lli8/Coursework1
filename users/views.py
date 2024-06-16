from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, UserSignInForm
from files.models import CustomFiles


def signin_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Неверный Email или пароль")
    else:
        form = UserSignInForm()

    return render(request, "users/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def account_view(request):
    files = CustomFiles.objects.filter(uploaded_by=request.user).all()
    return render(request, "users/account.html", {"files": files})


def contacts_view(request):
    return render(request, "users/contacts.html")


def help_view(request):
    return render(request, "users/contacts.html")
