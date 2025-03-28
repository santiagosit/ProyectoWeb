"""
URL configuration for ProyectoWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_usuarios.urls')),  # Mantener esta como ruta base
    path('productos/', include('app_inventario.urls')),
    path('finanzas/', include('app_finanzas.urls')),
    path('pedidos/', include('app_pedidos.urls')),
    path('ventas/', include('app_ventas.urls')),
    path('reportes/', include('app_reportes.urls')),
    path('eventos/', include('app_eventos.urls')),  # Cambiar a una ruta específica
    #path('pagos/', include('app_pagos.urls')),
]

