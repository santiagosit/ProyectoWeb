from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from functools import wraps
from .models import Profile

def is_admin_or_superuser(user):
    """Verifica si el usuario es admin o superusuario"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        profile = Profile.objects.get(user=user)
        return profile.rol == 'Administrador'
    except Profile.DoesNotExist:
        return False

def is_employee_or_above(user):
    """Verifica si el usuario es empleado, admin o superusuario"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    try:
        profile = Profile.objects.get(user=user)
        return profile.rol in ['Administrador', 'Empleado']
    except Profile.DoesNotExist:
        return False

def is_employee(user):
    """Verifica si el usuario es empleado"""
    if not user.is_authenticated:
        return False
    try:
        profile = Profile.objects.get(user=user)
        return profile.rol == 'Empleado'
    except Profile.DoesNotExist:
        return False

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_admin_or_superuser(request.user):
            return redirect('empleado_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        print(f"employee_required: user={request.user}, authenticated={request.user.is_authenticated}")
        if not is_employee_or_above(request.user):
            print(f"NO es empleado ni admin. user={request.user}, authenticated={request.user.is_authenticated}")
            # Si está autenticado pero no es empleado ni admin, redirige según rol
            if request.user.is_authenticated:
                if hasattr(request.user, 'profile'):
                    print(f"Tiene profile. Rol={getattr(request.user.profile, 'rol', None)}")
                    if request.user.profile.rol == 'Administrador':
                        print("Redirigiendo a home (admin)")
                        return redirect('home')  # Dashboard admin
                    elif request.user.profile.rol == 'Empleado':
                        print("Redirigiendo a empleado_dashboard")
                        return redirect('empleado_dashboard')  # Dashboard empleado
                    else:
                        print(f"Perfil con rol desconocido: {request.user.profile.rol}")
                else:
                    print("NO tiene profile asociado")
                # Usuario autenticado sin perfil válido: cerrar sesión y redirigir a login
                from django.contrib.auth import logout
                logout(request)
                print("Cerrando sesión y redirigiendo a login")
                return redirect('login')
            else:
                print("Usuario NO autenticado. Redirigiendo a login")
                return redirect('login')
        print("Acceso permitido a la vista protegida para empleado o admin")
        return view_func(request, *args, **kwargs)
    return _wrapped_view