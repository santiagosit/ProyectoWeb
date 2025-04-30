from django.urls import path
from . import views

app_name = 'predicciones'  # Asegúrate de que el app_name esté definido

urlpatterns = [    
    # Dashboard principal
    path('dashboard/', views.dashboard_predicciones, name='dashboard'),
    path('oportunidad-compra/', views.oportunidad_compra_prediccion, name='oportunidad_compra'),
    # Predicciones estacionales para productos alcohólico
]