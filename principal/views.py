from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Registro, Usuario  # Asegúrate de que Usuario es un modelo compatible con auth
from .forms import RegistroUsuarioForm
from django.contrib import messages

# Vista para el inicio de sesión
def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('registros')  # Redirige a la vista de registros después del login
    else:
        form = RegistroUsuarioForm()
    return render(request, 'principal/registro.html', {'form': form})

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
    registros = Registro.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'principal/registros.html', {'registros': registros})


# Vista para cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def actualizar_registro(request):
    if request.method == 'POST':
        registro_id = request.POST.get('id')
        try:
            registro = Registro.objects.get(id=registro_id, usuario=request.user)
            # Actualizamos los campos del registro
            registro.tipo_registro = request.POST.get('tipo_registro')
            registro.kilometraje = int(request.POST.get('kilometraje'))
            precio_str = request.POST.get('precio')
            # Reemplaza la coma por un punto para poder convertir a float
            precio_str = precio_str.replace(',', '.')
            # Ahora convierte a float
            precio = float(precio_str)
            registro.precio = precio
            registro.fecha = request.POST.get('fecha')
            registro.detalles = request.POST.get('detalles')


            # Guardamos el registro actualizado
            registro.save()

            # Mostrar mensaje de éxito
            messages.success(request, "Registro actualizado exitosamente.")
            return redirect('registros')  # Redirigir de nuevo a la página de registros
        except Registro.DoesNotExist:
            messages.error(request, "No se encontró el registro.")
            return redirect('registros')

    return redirect('registros')  # Redirigir si no es POST
