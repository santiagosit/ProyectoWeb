# Importaciones de Python
import random

# Importaciones de Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.utils.crypto import get_random_string

# Importaciones locales
from ProyectoWeb import settings
from .forms import UserForm, ProfileForm
from .models import Usuario, Profile, PIN
from .utils import is_admin_or_superuser, is_employee_or_above

# Vistas de autenticación
def login_view(request):
    """Vista para mostrar el formulario de inicio de sesión"""
    return render(request, 'usuarios/login.html')

def iniciar_sesion(request):
    """Vista para procesar el inicio de sesión"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'usuarios/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'usuarios/login.html')

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_employee_or_above)
def home(request):
    """Vista de la página principal"""
    return render(request, 'usuarios/home.html')

# Vistas de gestión de administradores
@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_administrador(request):
    """Vista para crear un nuevo administrador (solo superusuario)"""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.rol = 'Administrador'
            profile.save()
            return redirect('listar_administradores')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'usuarios/Administrador/crear_administrador.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_administradores(request):
    """Vista para listar todos los administradores"""
    administradores = Profile.objects.filter(rol='Administrador')
    return render(request, 'usuarios/Administrador/listar_administradores.html', {'administradores': administradores})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_administrador(request, admin_id):
    profile = get_object_or_404(Profile, id=admin_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=profile.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('listar_administradores')
    else:
        user_form = UserForm(instance=profile.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'usuarios/Administrador/edita r_administrador.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_administrador(request, admin_id):
    profile = get_object_or_404(Profile, id=admin_id)
    if request.method == 'POST':
        profile.user.delete()
        profile.delete()
        return redirect('listar_administradores')
    return render(request, 'usuarios/Administrador/eliminar_administrador.html', {'administrador': profile})

# Vistas de gestión de empleados
@login_required
@user_passes_test(is_admin_or_superuser)
def crear_empleado(request):
    """Vista para crear un nuevo empleado"""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.rol = 'Empleado'
            profile.save()
            return redirect('listar_empleados')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'usuarios/Empleado/crear_empleado.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
@user_passes_test(is_admin_or_superuser)
def listar_empleados(request):
    """Vista para listar todos los empleados"""
    empleados = Profile.objects.filter(rol='Empleado')
    return render(request, 'usuarios/Empleado/listar_empleados.html', {'empleados': empleados})

@login_required
@user_passes_test(is_admin_or_superuser)
def editar_empleado(request, empleado_id):
    profile = get_object_or_404(Profile, id=empleado_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=profile.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('listar_empleados')
    else:
        user_form = UserForm(instance=profile.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'usuarios/Empleado/editar_empleado.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
@user_passes_test(is_admin_or_superuser)
def eliminar_empleado(request, empleado_id):
    profile = get_object_or_404(Profile, id=empleado_id)
    if request.method == 'POST':
        profile.user.delete()
        profile.delete()
        return redirect('listar_empleados')
    return render(request, 'usuarios/Empleado/eliminar_empleado.html', {'empleado': profile})

# Vistas de recuperación de contraseña
def recuperar_password(request):
    """Vista para iniciar el proceso de recuperación de contraseña"""
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

def verificar_pin(request):
    """Vista para verificar el PIN de recuperación"""
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
    """Vista para restablecer la contraseña"""
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

# Funciones de utilidad
def generar_pin():
    """Genera un PIN aleatorio de 6 dígitos"""
    return str(random.randint(100000, 999999))

def enviar_pin(request):
    """Envía el PIN de recuperación por correo electrónico"""
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





