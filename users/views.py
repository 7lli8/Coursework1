from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserCreationForm, UserSignInForm


def signin_view(request):
    if request.user.is_authenticated:
        return redirect("")
    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
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
