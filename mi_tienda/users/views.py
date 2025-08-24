from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm

def user_login(request):
    if request.user.is_authenticated:
        return redirect('products:home')
    
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'products:home')
                messages.success(request, f'¡Bienvenido {user.username}!')
                return redirect(next_url)
        messages.error(request, 'Credenciales inválidas')
    else:
        form = CustomLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    messages.info(request, 'Has cerrado sesión exitosamente')
    logout(request)
    return redirect('users:login')