from django.urls import path
from . import views

app_name = 'predicciones'

urlpatterns = [
    # Redirigir la página principal a dashboard
    path('', views.dashboard_predicciones, name='index'),
    
    # Dashboard y API
    path('dashboard/', views.dashboard_predicciones, name='dashboard_predicciones'),
    path('api/datos-predicciones/', views.datos_predicciones_api, name='datos_predicciones_api'),
    
    # Predicciones
    path('lista/', views.lista_predicciones, name='lista_predicciones'),
    path('generar/', views.generar_predicciones, name='generar_predicciones'),
    path('detalle/<int:prediccion_id>/', views.detalle_prediccion, name='detalle_prediccion'),
    path('evaluar/<int:prediccion_id>/', views.evaluar_prediccion, name='evaluar_prediccion'),
    
    # Reportes y estadísticas
    path('estadisticas/', views.estadisticas_list, name='estadisticas_list'),
    path('productos-alta-rotacion/', views.productos_alta_rotacion, name='productos_alta_rotacion'),
    path('productos-baja-rotacion/', views.productos_baja_rotacion, name='productos_baja_rotacion'),
    path('oportunidades/', views.reporte_oportunidades, name='reporte_oportunidades'),
    path('tendencias/<int:producto_id>/', views.tendencias_producto, name='tendencias_producto'),
]