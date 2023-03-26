from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user_login.html', {'error_message': 'Usuário ou senha incorretos.'})
    else:
        return render(request, 'user_login.html')


def create_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            # exibir mensagem de erro
            return render(request, 'user_creation.html', {'error_message': 'As senhas não coincidem.'})
        try:
            User.objects.get(username=username)

            # exibir mensagem de erro
            return render(request, 'user_creation.html', {'error_message': 'O nome de usuário já está em uso.'})
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password1)
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'user_creation.html')