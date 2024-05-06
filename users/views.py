from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Здесь вы можете выполнить дополнительные действия после успешной регистрации
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('input')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})