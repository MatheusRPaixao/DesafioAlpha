from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Usuário ou senha incorretos.'})
    else:
        return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def create_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'sign-up.html', {'error_message': 'As senhas não coincidem.'})

        try:
            User.objects.get(username=username)

            return render(request, 'sign-up.html', {'error_message': 'O nome de usuário já está em uso.'})
        except User.DoesNotExist:
            User.objects.create_user(username, email, password1)

            user = authenticate(request, username=username, password=password1)
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'sign-up.html')