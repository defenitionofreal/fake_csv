from django.shortcuts import render
from .models import CustomUser
from .forms import LoginForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from csv_gen.views import dashboard


def user_login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('Data Schemas')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    request.session['user_id'] = user.id
                    login(request, user)
                    messages.success(request, 'Вы авторизовались')
                    return redirect('Data Schemas')
                else:
                    messages.error(request, 'Аккаунт не активен')
                    return render(request, 'login.html', {'form': form})
            else:
                messages.error(request, 'Неверный логин или пароль')
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('login')
