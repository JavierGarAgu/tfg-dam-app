from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Registro, User, Coche  # Asegúrate de que User es un model compatible con auth
from .forms import SignupUserForm
from django.contrib import messages
from datetime import datetime

# Vista para el inicio de sesión
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('registros')  # si ya está logueado te redirige
    if request.method == 'POST':
        form = SignupUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Coche.objects.create(
                user=user,
                brand='Toyota',      
                model='Por definir',
                year=2025,            
                engine='Por definir',
                fuel='gasolina'
            )
            login(request, user)
            return redirect('registros')  # Redirige a la vista de registros después del login
    else:
        form = SignupUserForm()
    return render(request, 'principal/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('registros')  # si ya está logueado te redirige
    
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')

        print(f"Intento de login: {user}")

        # Usar authenticate para verificar user y contraseña con hashes
        user = authenticate(request, username=user, password=password)

        if user is not None:
            print(f"juan existe: {user}")
            login(request, user)  # Autenticación y login exitoso
            next_url = request.GET.get('next', 'registros')
            return redirect(next_url)
        else:
            # Fallo de autenticación
            return render(request, 'principal/login.html', {'error': 'User o password incorrectos'})

    return render(request, 'principal/login.html')


# Vista para ver los registros del user autenticado
@login_required
def registros_view(request):
    coche = Coche.objects.get(user=request.user)
    
    # Obtener los registros del user autenticado
    registros = Registro.objects.filter(user=request.user).order_by('-date')
    
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
            coche = Coche.objects.get(id=coche_id, user=request.user)

            coche.brand = request.POST.get('brand')
            coche.model = request.POST.get('model')
            coche.year = int(request.POST.get('year'))
            coche.engine = request.POST.get('engine')
            coche.fuel = request.POST.get('fuel')

            coche.save()
            messages.success(request, "Coche actualizado exitosamente.")
            return redirect('info_coche')  # Redirige para evitar reenvío del formulario

        except Coche.DoesNotExist:
            messages.error(request, "No se encontró el coche.")
            return redirect('info_coche')

    # Si no es POST, simplemente muestra los coches
    coches = Coche.objects.filter(user=request.user)
    return render(request, 'principal/info_coche.html', {'coches': coches})


def nuevo_registro(request):
    if request.method == 'POST':
        registry_type = request.POST.get('registry_type')
        mileage = request.POST.get('mileage')
        price = request.POST.get('price')
        date = request.POST.get('date')
        details = request.POST.get('details')

  
        price_float = float(price.replace(',', '.'))  # Convertir ',' a '.' si es necesario
        nuevo = Registro.objects.create(
            registry_type=registry_type,
            mileage=int(mileage),
            price=price_float,
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            details=details,
            user=request.user
        )


    return render(request, 'principal/nuevo_registro.html')

@login_required
def actualizar_registro(request):
    if request.method == 'POST':
        registro_id = request.POST.get('id')

        registro = Registro.objects.get(id=registro_id, user=request.user)
        # Actualizamos los campos del registro
        registro.registry_type = request.POST.get('registry_type')
        registro.mileage = int(request.POST.get('mileage'))
        price_str = request.POST.get('price')
        # Reemplaza la coma por un punto para poder convertir a float
        price_str = price_str.replace(',', '.')
        # Ahora convierte a float
        price = float(price_str)
        registro.price = price
        registro.date = request.POST.get('date')
        registro.details = request.POST.get('details')


        # Guardamos el registro actualizado
        registro.save()

    return redirect('registros')  # Redirigir si no es POST

@login_required
def eliminar_registro(request, id):
    try:
        registro = Registro.objects.get(id=id, user=request.user)
        registro.delete()
        messages.success(request, "Registro eliminado correctamente.")
    except Registro.DoesNotExist:
        messages.error(request, "No se encontró el registro.")
    return redirect('registros')
