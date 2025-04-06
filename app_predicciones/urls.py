from django.urls import path
from . import views

app_name = 'predicciones'

urlpatterns = [
    path('', views.generar_predicciones, name='predicciones_list'),
    path('estadisticas/', views.actualizar_estadisticas, name='estadisticas_list'),
]