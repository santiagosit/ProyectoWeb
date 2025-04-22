from django.urls import path
from . import views

app_name = 'predicciones'  # Asegúrate de que el app_name esté definido

urlpatterns = [    
    path('predicciones/', views.dashboard_predicciones, name='dashboard_predicciones'),
]