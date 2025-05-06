from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Registro, Usuario
from django.contrib.auth.hashers import check_password  # Necesario para verificar passwords cifradas

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        # Agregar una línea de depuració
        print(f"Usuario ingresado: {usuario}, password ingresada: {password}")
        
        # Verificar si el usuario existe en la base de datos
        try:
            user = Usuario.objects.get(usuario=usuario)
            
            # Verificar si la password es correcta (ahora usando check_password)
            if check_password(password, user.password):  # Comparación de passwords cifradas
                # Si la autenticación es exitosa, iniciar sesión
                request.session['usuario_id'] = user.id
                return redirect('registros')  # Redirigir a la página de registros
            else:
                # Si la password es incorrecta, mostrar un error
                return render(request, 'principal/login.html', {'error': 'Usuario o password incorrectos'})
        except Usuario.DoesNotExist:
            # Si el usuario no existe, mostrar un error
            return render(request, 'principal/login.html', {'error': 'Usuario o password incorrectos'})
    
    return render(request, 'principal/login.html')


# Vista para ver los registros del usuario autenticado
@login_required
def registros_view(request):
    # Obtener los registros del usuario autenticado (usando request.user, que es el usuario logueado)
    registros = Registro.objects.filter(usuario=request.user)

    return render(request, 'principal/registros.html', {'registros': registros})

# Vista para cerrar sesión
@login_required
def logout_view(request):
    # Eliminar los datos de la sesión
    logout(request)
    return redirect('login')  # Redirigir al login
