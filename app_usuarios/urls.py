from django.urls import path
from . import views
from .views import recuperar_password, verificar_pin,enviar_pin
urlpatterns = [
    # Usuarios
    path('', views.login_view, name='login'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.iniciar_sesion, name='login'),
    path('home/', views.home, name='home'),
    path('recuperar/', views.recuperar_password, name='recuperar_password'),
    path('verificar_pin/', verificar_pin, name='verificar_pin'),
    path('enviar_pin/', enviar_pin, name='enviar_pin'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),
]
