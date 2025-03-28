from django.urls import path
from . import views
from .views import recuperar_password, verificar_pin,enviar_pin

urlpatterns = [
    # Usuarios
    path('', views.login_view, name='login'),
    path('login/', views.iniciar_sesion, name='login'),
    path('home/', views.home, name='home'),
    path('recuperar/', views.recuperar_password, name='recuperar_password'),
    path('verificar_pin/', views.verificar_pin, name='verificar_pin'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),

    # Administradores
    path('crear_administrador/', views.crear_administrador, name='crear_administrador'),
    path('listar_administradores/', views.listar_administradores, name='listar_administradores'),
    path('editar_administrador/<int:admin_id>/', views.editar_administrador, name='editar_administrador'),
    path('eliminar_administrador/<int:admin_id>/', views.eliminar_administrador, name='eliminar_administrador'),

    # Empleados - agregar prefijo 'empleados/'
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),
    path('empleados/editar/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
]
