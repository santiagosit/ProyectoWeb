import random

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from django.shortcuts import render,HttpResponse


from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from ProyectoWeb import settings
from .models import Usuario, PIN
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import PIN

from .models import Usuario

def login_view(request):
    return render(request, 'usuarios/login.html')
# views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth.models import User


def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save(commit=False)
            email = request.POST['email']  # Obtener el email del formulario
            nuevo_usuario.email = email  # Asignarlo al usuario
            nuevo_usuario.save()

            # Verificamos si el usuario ya existe para evitar duplicados
            usuario, created = Usuario.objects.get_or_create(
                email=nuevo_usuario.email,
                defaults={
                    'nombre': nuevo_usuario.username,
                    'password': nuevo_usuario.password,
                    'rol': 'Administrador',  # Suponiendo que el rol siempre es 'Administrador'
                }
            )

            # Si el usuario ya existe, actualizamos los detalles relevantes
            if not created:
                usuario.nombre = nuevo_usuario.username
                usuario.password = nuevo_usuario.password
                usuario.rol = 'Administrador'
                usuario.save()

            login(request, nuevo_usuario)
            return redirect('login')  # Redirige a la página principal después del registro

    else:
        form = UserCreationForm()

    return render(request, 'usuarios/registrar.html', {'form': form})

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Usuario


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Usuario


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Inicia la sesión del usuario
            return redirect('home')  # Redirige a una página principal home.html
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'usuarios/login.html')

def home(request):
    return render(request, 'usuarios/home.html')
def recuperar_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'usuarios/recuperar.html', {'error': 'El correo no está registrado.'})

            # Generar un nuevo PIN
            pin_code = get_random_string(6, allowed_chars='0123456789')

            # Crear o actualizar el PIN del usuario
            PIN.objects.update_or_create(user=user, defaults={'pin': pin_code})

            # Enviar el PIN al correo usando Amazon SES
            send_mail(
                'Recuperación de Contraseña',
                f'Tu PIN de recuperación es: {pin_code}',
                'santiagoproyectosemail@gmail.com',  # Cambia esto por la dirección de correo verificada
                [user.email],
                fail_silently=False,
            )
            return redirect('verificar_pin')
        else:
            return render(request, 'usuarios/recuperar.html', {'error': 'Por favor, introduce un correo electrónico.'})

    return render(request, 'usuarios/recuperar.html')


def generar_pin():
    return str(random.randint(100000, 999999))


def enviar_pin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'usuarios/recuperar.html', {'error': 'El correo no está registrado.'})

            # Generar un nuevo PIN
            pin_code = get_random_string(6, allowed_chars='0123456789')

            # Crear o actualizar el PIN del usuario
            PIN.objects.update_or_create(user=user, defaults={'pin': pin_code})

            # Enviar el PIN al correo usando Amazon SES
            send_mail(
                'Recuperación de Contraseña',
                f'Tu PIN de recuperación es: {pin_code}',
                'santiagoproyectosemail@gmail.com',  # Dirección de correo desde la que se envía
                [user.email],  # Dirección de correo del usuario que recibe el PIN
                fail_silently=False,
            )
            return redirect('verificar_pin')
        else:
            return render(request, 'usuarios/recuperar.html', {'error': 'Por favor, introduce un correo electrónico.'})

    return render(request, 'usuarios/recuperar.html')
def verificar_pin(request):
    if request.method == "POST":
        if 'email' in request.POST and 'pin' in request.POST:
            email = request.POST.get("email")
            pin = request.POST.get("pin")

            if email and pin:
                try:
                    user = User.objects.get(email=email)
                    pin_object = PIN.objects.get(user=user, pin=pin)

                    if pin_object.is_valid():
                        return render(request, 'usuarios/verificar_pin.html', {'email': email, 'valid_pin': True})

                    else:
                        return render(request, 'usuarios/verificar_pin.html', {'error': 'El PIN ha expirado.'})

                except (User.DoesNotExist, PIN.DoesNotExist):
                    return render(request, 'usuarios/verificar_pin.html', {'error': 'Correo o PIN incorrecto.'})

            return render(request, 'usuarios/verificar_pin.html', {'error': 'Por favor, completa todos los campos.'})

        elif 'new_password' in request.POST:
            new_password = request.POST.get('new_password')
            email = request.POST.get('email')

            if new_password and email:
                try:
                    user = User.objects.get(email=email)
                    # Validar la nueva contraseña usando las validaciones de Django
                    try:
                        validate_password(new_password, user)
                        user.set_password(new_password)
                        user.save()
                        return render(request, 'usuarios/verificar_pin.html',
                                      {'success': 'Contraseña cambiada exitosamente.', 'valid_pin': False})
                    except ValidationError as e:
                        return render(request, 'usuarios/verificar_pin.html',
                                      {'error': e.messages, 'valid_pin': True, 'email': email})

                except User.DoesNotExist:
                    return render(request, 'usuarios/verificar_pin.html',
                                  {'error': 'Usuario no encontrado.', 'valid_pin': True, 'email': email})

            else:
                return render(request, 'usuarios/verificar_pin.html',
                              {'error': 'Por favor, ingresa una nueva contraseña.', 'valid_pin': True, 'email': email})

    return render(request, 'usuarios/verificar_pin.html')
def reset_password(request, email):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        email = request.POST.get("email")

        if email and new_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return HttpResponse("Password reset successfully")
            except User.DoesNotExist:
                return HttpResponse("User not found")

    return render(request, 'usuarios/reset_password.html', {'email': email})
def logout_view(request):
    logout(request)
    return redirect('login')  # Puedes cambiar 'login' por cualquier otra página de redirección después del logout.





