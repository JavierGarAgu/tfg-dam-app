from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Registro, Usuario
from django.contrib.auth import authenticate

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        # Agregar una línea de depuración
        print(f"Usuario ingresado: {usuario}, password ingresada: {password}")
        
        try:
            # Buscar al usuario por su nombre
            user = Usuario.objects.get(usuario=usuario)
            
            # Comparar la contraseña en texto plano directamente
            if user.password == password:  # Comparación de contraseñas en texto plano
                # Si la autenticación es exitosa, iniciar sesión
                request.session['usuario_id'] = user.id
                login(request, user) 

                # Si el parámetro 'next' está en la URL, redirigir a esa URL después del login
                next_url = request.GET.get('next', 'registros')  # Si no hay 'next', redirigir a 'registros'
                print(f"ENTRA EN LOGIN: {usuario}, ENTRA EN LOGIN: {password}")
                return redirect(next_url)
            else:
                # Contraseña incorrecta
                return render(request, 'principal/login.html', {'error': 'Usuario o password incorrectos'})
        
        except Usuario.DoesNotExist:
            # Usuario no encontrado
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
