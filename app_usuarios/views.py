# Importaciones de Python
from pyexpat.errors import messages
import random
from django.utils import timezone


# Importaciones de Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction, IntegrityError  # Add IntegrityError here
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.timezone import localdate, now
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.db.models import Sum, F, Count  # Change this import
from decimal import Decimal

# Importaciones locales
from ProyectoWeb import settings
from app_finanzas.models import Egreso, Ingreso
from app_inventario.models import Producto
from app_inventario.views import get_productos_bajo_stock
from app_pedidos.models import Pedido
from app_ventas.models import Venta, VentaDetalle  # Añadir VentaDetalle
from app_eventos.models import Evento
from .forms import UserForm, ProfileForm
from .models import Profile, PIN
from .utils import is_admin_or_superuser, is_employee_or_above, employee_required
from datetime import datetime

# Vistas de autenticación
def login_view(request):
    """Vista para mostrar el formulario de inicio de sesión"""
    return render(request, 'usuarios/login.html')

def iniciar_sesion(request):
    """Vista para procesar el inicio de sesión"""
    import requests  # Asegura que requests esté importado
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # --- CAPTCHA Cloudflare Turnstile (comentado para desarrollo local) ---
        #captcha_response = request.POST.get('cf-turnstile-response')
        #captcha_valid = False
        #if captcha_response:
            #data = {
                #'secret': '0x4AAAAAABZGkfkDg9tcCC-UmNR8p3DGYWc',
                #'response': captcha_response,
                #'remoteip': request.META.get('REMOTE_ADDR')
            #}
            #r = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
            #captcha_valid = r.json().get('success', False)
        #if not captcha_valid:
            #messages.error(request, 'Verificación captcha fallida. Intenta de nuevo.')
            #return render(request, 'usuarios/login.html')
        # --- FIN CAPTCHA ---
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if hasattr(user, 'profile'):
                if user.profile.rol == 'Empleado':
                    return redirect('empleado_dashboard')
                elif user.profile.rol == 'Administrador' or user.is_superuser:
                    return redirect('home')
            messages.error(request, 'Usuario sin perfil asignado')
        else:
            messages.error(request, 'Credenciales incorrectas')
        return render(request, 'usuarios/login.html')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin_or_superuser, login_url='empleado_dashboard')
def home(request):
    print("Home view accessed")  # Debug log
    """Dashboard principal para administradores"""
    # Verificar que sea administrador o superusuario
    if not hasattr(request.user, 'profile') or (request.user.profile.rol != 'Administrador' and not request.user.is_superuser):
        # Si es empleado, redirigir a su dashboard
        if hasattr(request.user, 'profile') and request.user.profile.rol == 'Empleado':
            return redirect('empleado_dashboard')
        # Si no tiene perfil válido, cerrar sesión y redirigir a login
        logout(request)
        return redirect('login')
    

    #Tarjeta, envia información del total de ventas del dia
    hoy = localdate()  # Usa la zona horaria activa del proyecto
    ventas_hoy = Venta.objects.filter(fecha_creacion__date=hoy, estado='Completada')

    total_ventas_hoy = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas_hoy = ventas_hoy.count()


    #Tarjeta ventas totatles del mes
    inicio_mes = datetime(hoy.year, hoy.month, 1)

    # Sumar total de ventas completadas del mes actual
    total_ventas_mes = Venta.objects.filter(
        estado='completada',
        fecha_creacion__gte=inicio_mes
    ).aggregate(total_mes=Sum('total'))['total_mes'] or 0


    #Tarjeta ingresos y egresos del mes
    # Totales del mes actual
    total_ingresos_mes = Ingreso.objects.filter(
        fecha__gte=inicio_mes,
        fecha__lte=hoy
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    total_egresos_mes = Egreso.objects.filter(
        fecha__gte=inicio_mes,
        fecha__lte=hoy
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    balance_mes = total_ingresos_mes - total_egresos_mes
        

    # Tarjeta con productos con bajo stock
    productos_stock_bajo = Producto.objects.filter(cantidad_stock__lt=F('stock_minimo'))

    # Obtener pedidos con estado "pedido" o "en camino"
    pedidos_pendientes = Pedido.objects.filter(estado__in=['pedido', 'en camino']).order_by('fecha_pedido')

    # Productos más vendidos del mes
    productos_mas_vendidos = VentaDetalle.objects.filter(
        venta__fecha_creacion__gte=inicio_mes,
        venta__estado='Completada'
    ).values('producto__nombre').annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:5]  # Limitar a los 5 más vendidos
    
    # Obtener eventos próximos (pendientes o confirmados)
    eventos_proximos = Evento.objects.filter(
        estado__in=['Pendiente', 'Confirmado'],
        fecha_evento__gte=now()
    ).order_by('fecha_evento')[:5]  # Limitar a los 5 próximos eventos

    context = {
        'total_ventas_hoy': total_ventas_hoy,
        'cantidad_ventas_hoy': cantidad_ventas_hoy,
        'total_ventas_mes': total_ventas_mes,
        'total_ingresos_mes': total_ingresos_mes,
        'total_egresos_mes': total_egresos_mes,
        'balance_mes': balance_mes,
        'productos_stock_bajo': productos_stock_bajo,
        'pedidos_pendientes': pedidos_pendientes,
        'productos_mas_vendidos': productos_mas_vendidos,
        'eventos_proximos': eventos_proximos,
    }   
    return render(request, 'home.html', context)

@employee_required
# Elimina los decoradores antiguos para evitar doble chequeo
#@login_required
#@user_passes_test(is_employee_or_above)
def empleado_dashboard(request):
    """Dashboard para empleados"""
    # Verificar que sea empleado
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'Empleado':
        return redirect('home')
    
    # Obtener la fecha actual
    hoy = localdate()

    # Filtrar las ventas realizadas por el empleado en el día actual
    ventas_hoy = Venta.objects.filter(
        empleado=request.user.profile,
        fecha_creacion__date=hoy,
        estado='Completada'
    )

    # Calcular el total de ventas del día
    total_ventas_hoy = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas_hoy = ventas_hoy.count()

    # Filtrar las ventas realizadas por el empleado en el mes actual
    ventas_mes = Venta.objects.filter(
        empleado=request.user.profile,
        fecha_creacion__year=hoy.year,
        fecha_creacion__month=hoy.month,
        estado='Completada'
    )

    # Calcular el total de ventas del mes
    total_ventas_mes = ventas_mes.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas_mes = ventas_mes.count()

    # Obtener las últimas 5 ventas realizadas por el empleado
    ultimas_ventas = Venta.objects.filter(
        empleado=request.user.profile
    ).order_by('-fecha_creacion')[:5]

    # Calcular los productos más vendidos por el empleado
    productos_mas_vendidos = (
        VentaDetalle.objects.filter(venta__empleado=request.user.profile)
        .values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')[:5]
    )

    # Contexto para el template
    context = {
        'total_ventas_hoy': total_ventas_hoy,
        'cantidad_ventas_hoy': cantidad_ventas_hoy,
        'total_ventas_mes': total_ventas_mes,
        'cantidad_ventas_mes': cantidad_ventas_mes,
        'ultimas_ventas': ultimas_ventas,
        'productos_mas_vendidos': productos_mas_vendidos,  # Pasar los productos más vendidos al contexto
    }

    return render(request, 'usuarios/empleado_dashboard.html', context)



# Vistas de gestión de administradores
@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_administrador(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        print("Processing form submission...")  # Debug log
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    # Create user first
                    user = user_form.save()
                    
                    # Delete existing profile if it exists
                    Profile.objects.filter(user=user).delete()
                    
                    # Create new profile
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.rol = 'Administrador'
                    profile.save()
                    
                    print(f"Administrator created successfully: {user.username}")  # Debug log
                    return redirect('listar_administradores')
                    
            except IntegrityError as e:
                print(f"IntegrityError: {e}")  # Debug log
                user.delete()  # Rollback user creation
                user_form.add_error(None, f"Error al crear el administrador: {str(e)}")
            except Exception as e:
                print(f"Unexpected error: {e}")  # Debug log
                if 'user' in locals():
                    user.delete()  # Rollback user creation
                user_form.add_error(None, f"Error inesperado al crear el administrador: {str(e)}")
        else:
            print("Form validation errors:")  # Debug log
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    
    return render(request, 'usuarios/Administrador/crear_administrador.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'form_errors': user_form.errors or profile_form.errors,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_administradores(request):
    administradores = Profile.objects.filter(
        rol='Administrador',
        user__is_superuser=False  # Excluir superusuarios
    )
    
    # Aplicar filtros
    nombre = request.GET.get('nombre', '')
    email = request.GET.get('email', '')
    telefono = request.GET.get('telefono', '')

    if nombre:
        administradores = administradores.filter(nombre_completo__icontains=nombre)
    if email:
        administradores = administradores.filter(user__email__icontains=email)
    if telefono:
        administradores = administradores.filter(telefono__icontains(telefono))

    return render(request, 'usuarios/Administrador/listar_administradores.html', {
        'administradores': administradores
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_administrador(request, admin_id):
    admin = get_object_or_404(Profile, id=admin_id)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=admin.user, edit_mode=True)
        profile_form = ProfileForm(request.POST, instance=admin)
        
        if user_form.is_valid() and profile_form.is_valid():
            request.session['admin_edit_data'] = {
                'username': user_form.cleaned_data['username'],
                'email': user_form.cleaned_data['email'],
                'nombre_completo': profile_form.cleaned_data['nombre_completo'],
                'telefono': profile_form.cleaned_data['telefono'],
                'direccion': profile_form.cleaned_data['direccion'],
                'password': user_form.cleaned_data.get('password', ''),
                'rol': admin.rol
            }
            return redirect('confirmar_edicion_admin', admin_id=admin.id)
    else:
        user_form = UserForm(instance=admin.user, edit_mode=True)
        profile_form = ProfileForm(instance=admin)
    
    return render(request, 'usuarios/Administrador/editar_administrador.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'admin': admin
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def confirmar_edicion_admin(request, admin_id):
    admin = get_object_or_404(Profile, id=admin_id)
    new_data = request.session.get('admin_edit_data', {})

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update user data
                user = admin.user
                user.username = new_data.get('username', user.username)
                user.email = new_data.get('email', user.email)
                
                if new_data.get('password'):
                    user.set_password(new_data['password'])
                
                user.save()

                # Update profile data
                admin.nombre_completo = new_data.get('nombre_completo', admin.nombre_completo)
                admin.telefono = new_data.get('telefono', admin.telefono)
                admin.direccion = new_data.get('direccion', admin.direccion)
                admin.save()

                # Clear session data
                if 'admin_edit_data' in request.session:
                    del request.session['admin_edit_data']

                messages.success(request, '¡Administrador actualizado exitosamente!')
                return redirect('listar_administradores')

        except Exception as e:
            messages.error(request, f'Error al actualizar el administrador: {str(e)}')
            return redirect('editar_administrador', admin_id=admin.id)

    return render(request, 'usuarios/Administrador/confirmar_edicion_admin.html', {
        'admin': admin,
        'new_data': new_data,
        'show_password_change': bool(new_data.get('password'))
    })

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
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    # Check for existing email globally
                    email = user_form.cleaned_data['email']
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Este correo electrónico ya está registrado')
                        return render(request, 'usuarios/Empleado/crear_empleado.html', {
                            'user_form': user_form,
                            'profile_form': profile_form
                        })

                    # Create the user
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.save()
                    
                    # Store data for confirmation
                    request.session['empleado_temp_data'] = {
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'nombre_completo': profile_form.cleaned_data['nombre_completo'],
                        'telefono': profile_form.cleaned_data['telefono'],
                        'direccion': profile_form.cleaned_data['direccion'],
                        'fecha_contratacion': profile_form.cleaned_data['fecha_contratacion'].strftime('%Y-%m-%d')
                    }
                    
                    return redirect('confirmar_creacion_empleado')
                    
            except Exception as e:
                messages.error(request, f'Error al crear el empleado: {str(e)}')
                if 'user' in locals():
                    user.delete()
        else:
            for form in [user_form, profile_form]:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    
    return render(request, 'usuarios/Empleado/crear_empleado.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@user_passes_test(is_admin_or_superuser)
def confirmar_creacion_empleado(request):
    temp_data = request.session.get('empleado_temp_data', {})
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # First check if the user still exists (might have been deleted)
                try:
                    user = User.objects.get(id=temp_data['user_id'])
                except User.DoesNotExist:
                    messages.error(request, 'Error: El usuario no existe')
                    return redirect('crear_empleado')

                # Check if profile already exists
                if hasattr(user, 'profile'):
                    user.delete()
                    messages.error(request, 'Error: Ya existe un perfil para este usuario')
                    return redirect('crear_empleado')

                # Create the profile
                profile = Profile(
                    user=user,
                    rol='Empleado',
                    nombre_completo=temp_data['nombre_completo'],
                    telefono=temp_data['telefono'],
                    direccion=temp_data['direccion'],
                    fecha_contratacion=temp_data['fecha_contratacion']
                )
                profile.save()
                
                # Clear the session data
                if 'empleado_temp_data' in request.session:
                    del request.session['empleado_temp_data']
                
                messages.success(request, 'Empleado creado exitosamente')
                return redirect('listar_empleados')
                
        except IntegrityError as e:
            # If something goes wrong, delete the user to prevent orphaned users
            if 'user' in locals():
                user.delete()
            messages.error(request, 'Error: Ya existe un perfil para este usuario')
            return redirect('crear_empleado')
        except Exception as e:
            if 'user' in locals():
                user.delete()    
            messages.error(request, f'Error al crear el empleado: {str(e)}')
            return redirect('crear_empleado')
    
    return render(request, 'usuarios/Empleado/confirmar_creacion_empleado.html', {
        'data': temp_data
    })

@login_required
@user_passes_test(is_admin_or_superuser)
def listar_empleados(request):
    """Vista para listar todos los empleados"""
    empleados = Profile.objects.filter(rol='Empleado')
    
    # Aplicar filtros
    nombre = request.GET.get('nombre', '')
    email = request.GET.get('email', '')
    telefono = request.GET.get('telefono', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    if nombre:
        empleados = empleados.filter(nombre_completo__icontains=nombre)
    if email:
        empleados = empleados.filter(user__email__icontains=email)
    if telefono:
        empleados = empleados.filter(telefono__icontains(telefono))
    if fecha_desde:
        empleados = empleados.filter(fecha_contratacion__gte=fecha_desde)
    if fecha_hasta:
        empleados = empleados.filter(fecha_contratacion__lte=fecha_hasta)

    return render(request, 'usuarios/Empleado/listar_empleados.html', {
        'empleados': empleados
    })

@login_required
@user_passes_test(is_admin_or_superuser)
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Profile, id=empleado_id, rol='Empleado')
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=empleado.user, edit_mode=True)
        profile_form = ProfileForm(request.POST, instance=empleado)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                request.session['empleado_edit_data'] = {
                    'username': user_form.cleaned_data['username'],
                    'email': user_form.cleaned_data['email'],
                    'nombre_completo': profile_form.cleaned_data['nombre_completo'],
                    'telefono': profile_form.cleaned_data['telefono'],
                    'direccion': profile_form.cleaned_data['direccion'],
                    'fecha_contratacion': profile_form.cleaned_data['fecha_contratacion'].strftime('%Y-%m-%d'),
                    'password': user_form.cleaned_data.get('password', '')
                }
                return redirect('confirmar_edicion_empleado', empleado_id=empleado.id)
            except IntegrityError:
                messages.error(request, 'Error: Ya existe un usuario con ese nombre de usuario o correo electrónico')
        else:
            for form in [user_form, profile_form]:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        # Inicializar los formularios con los datos existentes
        user_form = UserForm(instance=empleado.user, edit_mode=True)
        profile_form = ProfileForm(instance=empleado)
    
    return render(request, 'usuarios/Empleado/editar_empleado.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'empleado': empleado
    })

@login_required
@user_passes_test(is_admin_or_superuser)
def eliminar_empleado(request, empleado_id):
    profile = get_object_or_404(Profile, id=empleado_id)
    if request.method == 'POST':
        profile.user.delete()
        profile.delete()
        return redirect('listar_empleados')
    return render(request, 'usuarios/Empleado/eliminar_empleado.html', {'empleado': profile})

@login_required
@user_passes_test(is_admin_or_superuser)
def confirmar_edicion_empleado(request, empleado_id):
    empleado = get_object_or_404(Profile, id=empleado_id)
    new_data = request.session.get('empleado_edit_data', {})
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user = empleado.user
                user.username = new_data.get('username', user.username)
                user.email = new_data.get('email', user.email)
                if new_data.get('password'):
                    user.set_password(new_data['password'])
                user.save()

                empleado.nombre_completo = new_data.get('nombre_completo', empleado.nombre_completo)
                empleado.telefono = new_data.get('telefono', empleado.telefono)
                empleado.direccion = new_data.get('direccion', empleado.direccion)
                empleado.fecha_contratacion = new_data.get('fecha_contratacion', empleado.fecha_contratacion)
                empleado.save()

                if 'empleado_edit_data' in request.session:
                    del request.session['empleado_edit_data']

                messages.success(request, '¡Empleado actualizado exitosamente!')
                return redirect('listar_empleados')

        except IntegrityError as e:
            messages.error(request, f'Error de integridad: {str(e)}')
            return redirect('editar_empleado', empleado_id=empleado.id)
        except Exception as e:
            messages.error(request, f'Error al actualizar el empleado: {str(e)}')
            return redirect('editar_empleado', empleado_id=empleado.id)

    return render(request, 'usuarios/Empleado/confirmar_edicion_empleado.html', {
        'empleado': empleado,
        'new_data': new_data
    })

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
            PIN.objects.update_or_create(user=user, defaults={'pin': pin_code, 'created_at': timezone.now()})

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

def enviar_pin(request):
    """Envía el PIN de recuperación por correo electrónico"""
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'El correo no se encuentra registrado')
                return render(request, 'usuarios/recuperar.html')
            # Generar un nuevo PIN
            pin_code = get_random_string(6, allowed_chars='0123456789')

            # Crear o actualizar el PIN del usuario
            PIN.objects.update_or_create(user=user, defaults={'pin': pin_code, 'created_at': timezone.now()})

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
            messages.error(request, 'Por favor, introduce un correo electrónico.')
            return render(request, 'usuarios/recuperar.html')
    return render(request, 'usuarios/recuperar.html')

def verificar_pin(request):
    """Vista para verificar el PIN de recuperación"""
    if request.method == "POST":
        if 'pin' in request.POST and 'email' in request.POST:
            email = request.POST.get('email')
            pin = request.POST.get('pin')
            if email and pin:
                try:
                    user = User.objects.get(email=email)
                    pin_obj = PIN.objects.get(user=user, pin=pin)
                    if pin_obj and not pin_obj.is_expired():
                        return render(request, 'usuarios/verificar_pin.html', {'email': email, 'valid_pin': True})
                    else:
                        messages.error(request, 'PIN o correo no válido.')
                        return render(request, 'usuarios/verificar_pin.html')
                except (User.DoesNotExist, PIN.DoesNotExist):
                    messages.error(request, 'PIN o correo no válido.')
                    return render(request, 'usuarios/verificar_pin.html')
            else:
                messages.error(request, 'Por favor, completa todos los campos.')
                return render(request, 'usuarios/verificar_pin.html')
        elif 'new_password' in request.POST:
            new_password = request.POST.get('new_password')
            email = request.POST.get('email')
            if new_password and email:
                try:
                    user = User.objects.get(email=email)
                    try:
                        validate_password(new_password, user)
                        user.set_password(new_password)
                        user.save()
                        return render(request, 'usuarios/verificar_pin.html', {'success': 'Contraseña cambiada exitosamente.', 'valid_pin': False})
                    except ValidationError as e:
                        messages.error(request, e.messages[0] if e.messages else 'Contraseña no válida.')
                        return render(request, 'usuarios/verificar_pin.html', {'valid_pin': True, 'email': email})
                except User.DoesNotExist:
                    messages.error(request, 'PIN o correo no válido.')
                    return render(request, 'usuarios/verificar_pin.html', {'valid_pin': True, 'email': email})
            else:
                messages.error(request, 'Por favor, ingresa una nueva contraseña.')
                return render(request, 'usuarios/verificar_pin.html', {'valid_pin': True, 'email': email})
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

# --- Vista personalizada para 404 ---
from django.shortcuts import render

def custom_404_view(request, exception):
    """Muestra una página 404 personalizada sin header/base si el usuario no está autenticado"""
    if not request.user.is_authenticated:
        # Muestra el 404 minimalista para usuarios no logueados
        return render(request, 'usuarios/404.html', status=404)
    else:
        # Si está logueado, puedes mostrar otra plantilla o el mismo 404 pero extendiendo de base normal si lo deseas
        return render(request, 'usuarios/404.html', status=404)

# Funciones de utilidad
def generar_pin():
    """Genera un PIN aleatorio de 6 dígitos"""
    return str(random.randint(100000, 999999))
