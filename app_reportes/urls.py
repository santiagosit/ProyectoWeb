from django.urls import path
from . import views
from .views import reporte_ingresos_egresos

urlpatterns = [
    path('reporte/', views.reporte_inventario, name='reporte_inventario'),
    path('reporte/excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),
path('reporte-ingresos-egresos/', reporte_ingresos_egresos, name='reporte_ingresos_egresos'),
]