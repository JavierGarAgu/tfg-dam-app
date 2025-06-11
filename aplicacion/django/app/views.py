from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Registro, Usuario, Coche  # Asegúrate de que Usuario es un modelo compatible con auth
from .forms import SignupUsuarioForm
from django.contrib import messages
from datetime import datetime

# Vista para el inicio de sesión
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('registros')  # si ya está logueado te redirige
    if request.method == 'POST':
        form = SignupUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Coche.objects.create(
                usuario=usuario,
                marca='*',      
                modelo='Por definir',
                año=2025,            
                motor='Por definir',
                combustible='*'
            )
            login(request, usuario)
            return redirect('registros')  # Redirige a la vista de registros después del login
    else:
        form = SignupUsuarioForm()
    return render(request, 'principal/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('registros')  # si ya está logueado te redirige
    
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
    coche = Coche.objects.get(usuario=request.user)
    
    # Obtener los registros del usuario autenticado
    registros = Registro.objects.filter(usuario=request.user).order_by('-fecha')
    
    # Pasar tanto los registros como el coche al template
    return render(request, 'principal/registros.html', {'registros': registros, 'coche': coche})


# Vista para cerrar sesión
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def info_coche(request):
    if request.method == 'POST':
        coche_id = request.POST.get('id')
        try:
            coche = Coche.objects.get(id=coche_id, usuario=request.user)

            coche.marca = request.POST.get('marca')
            coche.modelo = request.POST.get('modelo')
            coche.año = int(request.POST.get('año'))
            coche.motor = request.POST.get('motor')
            coche.combustible = request.POST.get('combustible')

            coche.save()
            messages.success(request, "Coche actualizado exitosamente.")
            return redirect('info_coche')  # Redirige para evitar reenvío del formulario

        except Coche.DoesNotExist:
            messages.error(request, "No se encontró el coche.")
            return redirect('info_coche')

    # Si no es POST, simplemente muestra los coches
    coches = Coche.objects.filter(usuario=request.user)
    return render(request, 'principal/info_coche.html', {'coches': coches})


def nuevo_registro(request):
    if request.method == 'POST':
        tipo_registro = request.POST.get('tipo_registro')
        kilometraje = request.POST.get('kilometraje')
        precio = request.POST.get('precio')
        fecha = request.POST.get('fecha')
        detalles = request.POST.get('detalles')

  
        precio_float = float(precio.replace(',', '.'))  # Convertir ',' a '.' si es necesario
        nuevo = Registro.objects.create(
            tipo_registro=tipo_registro,
            kilometraje=int(kilometraje),
            precio=precio_float,
            fecha=datetime.strptime(fecha, '%Y-%m-%d').date(),
            detalles=detalles,
            usuario=request.user
        )


    return render(request, 'principal/nuevo_registro.html')

@login_required
def actualizar_registro(request):
    if request.method == 'POST':
        registro_id = request.POST.get('id')

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

    return redirect('registros')  # Redirigir si no es POST

@login_required
def eliminar_registro(request, id):
    try:
        registro = Registro.objects.get(id=id, usuario=request.user)
        registro.delete()
        messages.success(request, "Registro eliminado correctamente.")
    except Registro.DoesNotExist:
        messages.error(request, "No se encontró el registro.")
    return redirect('registros')
