from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from app_inventario.models import Producto
from app_ventas.models import VentaDetalle

@login_required
def dashboard_predicciones(request):
    hoy = timezone.now()
    hace_4_semanas = hoy - timedelta(weeks=4)
    detalles = VentaDetalle.objects.filter(venta__fecha_creacion__gte=hace_4_semanas)

    productos = Producto.objects.all()
    predicciones_entre_semana = []
    predicciones_fin_de_semana = []

    for producto in productos:
        entre_semana = detalles.filter(
            producto=producto,
            venta__fecha_creacion__week_day__in=[2, 3, 4, 5]  # Lunes a Jueves
        ).aggregate(total=Sum('cantidad'))['total'] or 0  

        fin_de_semana = detalles.filter(
            producto=producto,
            venta__fecha_creacion__week_day__in=[6, 7, 1]  # Viernes a Domingo
        ).aggregate(total=Sum('cantidad'))['total'] or 0 

        promedio_entre_semana = entre_semana // 4
        promedio_fin_de_semana = fin_de_semana // 4

        stock_actual = producto.cantidad_stock
        stock_minimo = producto.stock_minimo

        predicciones_entre_semana.append({
            'producto': producto.nombre,
            'stock_actual': stock_actual,
            'stock_minimo': stock_minimo,
            'promedio_semanal': promedio_entre_semana,
            'cantidad_sugerida': max(promedio_entre_semana - stock_actual, 0)
        })

        predicciones_fin_de_semana.append({
            'producto': producto.nombre,
            'stock_actual': stock_actual,
            'stock_minimo': stock_minimo,
            'promedio_semanal': promedio_fin_de_semana,
            'cantidad_sugerida': max(promedio_fin_de_semana - stock_actual, 0)
        })

    context = {
        'entre_semana': predicciones_entre_semana,
        'fin_de_semana': predicciones_fin_de_semana
    }
    return render(request, 'predicciones/dashboard.html', context)
