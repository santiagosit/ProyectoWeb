from django.urls import path
from . import views

urlpatterns = [
    path('ingresos/', views.listar_ingresos, name='listar_ingresos'),
    path('egresos/', views.listar_egresos, name='listar_egresos'),
    path('ingresos/<int:ingreso_id>/', views.detalle_ingreso, name='detalle_ingreso'),
    path('egresos/<int:egreso_id>/', views.detalle_egreso, name='detalle_egreso'),
path('egresos/crear_personalizado/', views.crear_egreso_personalizado, name='crear_egreso_personalizado'),
    path('egresos/<int:egreso_id>/detalle/', views.detalle_egreso, name='detalle_egreso'),
    path('egresos/<int:egreso_id>/eliminar/', views.eliminar_egreso_personalizado,
         name='eliminar_egreso_personalizado'),
]
