from django.urls import path
from . import views

urlpatterns = [
    # Vistas principales
    path('', views.dashboard_predicciones, name='dashboard_predicciones'),
    path('lista/', views.lista_predicciones, name='lista_predicciones'),
    path('detalle/<int:prediccion_id>/', views.detalle_prediccion, name='detalle_prediccion'),
    path('generar/', views.generar_predicciones, name='generar_predicciones'),
    path('evaluar/<int:prediccion_id>/', views.evaluar_prediccion, name='evaluar_prediccion'),
    
    # Vistas de reportes específicos
    path('baja-rotacion/', views.productos_baja_rotacion, name='productos_baja_rotacion'),
    path('alta-rotacion/', views.productos_alta_rotacion, name='productos_alta_rotacion'),
    path('reporte-oportunidades/', views.reporte_oportunidades, name='reporte_oportunidades'),
    path('tendencias/<int:producto_id>/', views.tendencias_producto, name='tendencias_producto'),
    
    # API para datos de gráficas
    path('api/datos-predicciones/', views.datos_predicciones_api, name='datos_predicciones_api'),
]