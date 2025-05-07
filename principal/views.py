from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Registro, Usuario  # Asegúrate de que Usuario es un modelo compatible con auth

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        print(f"Intento de login: {usuario}")

        # Usar authenticate para verificar usuario y contraseña con hashes
        user = authenticate(request, username=usuario, password=password)

        if user is not None:
            print(f"juan existe: {usuario}")
            login(request, user)  # Autenticación y login exitoso

            next_url = request.GET.get('next', 'registros')
            return redirect(next_url)
        else:
            # Fallo de autenticación
            return render(request, 'principal/login.html', {'error': 'Usuario o password incorrectos'})

    return render(request, 'principal/login.html')


# Vista para ver los registros del usuario autenticado
@login_required
def registros_view(request):
    registros = Registro.objects.filter(usuario=request.user)
    return render(request, 'principal/registros.html', {'registros': registros})


# Vista para cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
