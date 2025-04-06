from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, F, ExpressionWrapper, fields
from django.db.models.functions import ExtractMonth, Now
from datetime import datetime, timedelta
from decimal import Decimal
from .models import PrediccionVenta, EstadisticaVenta
from app_ventas.models import VentaDetalle
from app_inventario.models import Producto

def calcular_tendencia(promedio_actual, promedio_anterior):
    # Si no hay datos históricos, evaluamos con más precisión
    if promedio_anterior == 0:
        # Si hay ventas actuales pero no históricas, podría ser un producto nuevo con potencial
        if promedio_actual > 3:  # Si las ventas son significativas (umbral reducido)
            return 'alta'
        elif promedio_actual > 1:  # Si hay ventas moderadas (umbral reducido)
            return 'media'
        elif promedio_actual > 0:  # Si hay algunas ventas
            return 'baja'
        # Si no hay ventas actuales ni históricas, consideramos riesgo
        return 'riesgo'
    
    # Calcular variación porcentual
    variacion = ((promedio_actual - promedio_anterior) / promedio_anterior) * 100
    
    # Criterios ajustados para obtener una distribución más equilibrada de tendencias
    if variacion > 20:  # Crecimiento significativo
        return 'alta'
    elif variacion >= 5:  # Crecimiento moderado
        return 'alta'
    elif variacion >= -5:  # Estabilidad relativa
        return 'media'
    elif variacion >= -20:  # Disminución moderada
        return 'baja'
    else:  # Disminución significativa
        return 'riesgo'

def calcular_cantidad_sugerida(producto, tendencia, promedio_ventas):
    # Calcular días de stock basado en el promedio de ventas diarias
    dias_stock_objetivo = 30  # Por defecto, mantener stock para un mes
    
    # Ajustar días de stock según la tendencia
    if tendencia == 'alta':
        # Para tendencia alta, mantener más stock para satisfacer demanda creciente
        dias_stock_objetivo = 45  # 1.5 meses
        factor_multiplicador = 1.4
    elif tendencia == 'media':
        # Para tendencia media, mantener stock equilibrado
        dias_stock_objetivo = 30  # 1 mes
        factor_multiplicador = 1.2
    elif tendencia == 'baja':
        # Para tendencia baja, reducir stock pero mantener suficiente
        dias_stock_objetivo = 20  # 0.67 meses
        factor_multiplicador = 0.9
    else:  # riesgo
        # Para riesgo, minimizar stock
        dias_stock_objetivo = 15  # 0.5 meses
        factor_multiplicador = 0.7
    
    # Calcular cantidad base según promedio de ventas y factor multiplicador
    cantidad_base = int(promedio_ventas * factor_multiplicador * dias_stock_objetivo)
    
    # Considerar stock mínimo como límite inferior
    cantidad_sugerida = max(cantidad_base, producto.stock_minimo)
    
    # Considerar el tiempo de reposición (lead time) si está disponible
    # Asumimos un tiempo de reposición de 7 días como ejemplo
    tiempo_reposicion = 7
    stock_seguridad = int(promedio_ventas * tiempo_reposicion * 1.5)  # 50% extra como seguridad
    
    # La cantidad final debe cubrir el stock de seguridad
    return max(cantidad_sugerida, stock_seguridad, producto.stock_minimo)

@login_required
def generar_predicciones(request):
    fecha_actual = datetime.now().date()
    mes_anterior = fecha_actual - timedelta(days=30)
    dos_meses_atras = fecha_actual - timedelta(days=60)
    tres_meses_atras = fecha_actual - timedelta(days=90)  # Añadimos análisis de 3 meses para mejorar predicciones

    # Obtener parámetros de filtrado
    tendencia_filtro = request.GET.get('tendencia', '')
    busqueda = request.GET.get('busqueda', '')
    
    # Iniciar con todos los productos
    productos = Producto.objects.all()
    
    # Filtrar por nombre si se proporciona búsqueda
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
        
    predicciones = []

    for producto in productos:
        # Ventas del último mes - solo ventas completadas
        ventas_mes_actual = VentaDetalle.objects.filter(
            producto=producto,
            venta__estado='completada',  # Solo considerar ventas completadas
            venta__fecha_creacion__date__gte=mes_anterior,
            venta__fecha_creacion__date__lte=fecha_actual
        ).aggregate(
            total_vendido=Sum('cantidad'),
            total_ingresos=Sum('precio_total')  # Añadimos total de ingresos para análisis
        )
        
        # Calcular el promedio diario correctamente (total vendido / número de días)
        dias_periodo = (fecha_actual - mes_anterior).days or 1  # Evitar división por cero
        promedio_diario_actual = (ventas_mes_actual['total_vendido'] or 0) / dias_periodo

        # Ventas del mes anterior para comparación - solo ventas completadas
        ventas_mes_anterior = VentaDetalle.objects.filter(
            producto=producto,
            venta__estado='completada',  # Solo considerar ventas completadas
            venta__fecha_creacion__date__gte=dos_meses_atras,
            venta__fecha_creacion__date__lt=mes_anterior
        ).aggregate(
            total_vendido=Sum('cantidad')
        )
        
        # Calcular el promedio diario correctamente para el mes anterior
        dias_periodo_anterior = (mes_anterior - dos_meses_atras).days or 1  # Evitar división por cero
        promedio_diario_anterior = (ventas_mes_anterior['total_vendido'] or 0) / dias_periodo_anterior
        
        # Ventas de hace 2-3 meses para análisis de tendencia a largo plazo
        ventas_tres_meses = VentaDetalle.objects.filter(
            producto=producto,
            venta__estado='completada',
            venta__fecha_creacion__date__gte=tres_meses_atras,
            venta__fecha_creacion__date__lt=dos_meses_atras
        ).aggregate(total_vendido=Sum('cantidad'))

        # Usar los promedios diarios calculados correctamente
        promedio_actual = promedio_diario_actual
        promedio_anterior = promedio_diario_anterior
        total_tres_meses = ventas_tres_meses['total_vendido'] or 0

        # Mejorar cálculo de tendencia considerando datos de 3 meses
        tendencia = calcular_tendencia(promedio_actual, promedio_anterior)
        cantidad_sugerida = calcular_cantidad_sugerida(producto, tendencia, promedio_actual)

        # Mejorar cálculo de confianza basado en más factores
        confianza = 0.4  # Base confidence más optimista
        
        # Aumentar confianza si hay datos consistentes
        if promedio_actual > 0:
            confianza += 0.2
        if promedio_anterior > 0:
            confianza += 0.15
        if total_tres_meses > 0:
            confianza += 0.1
            
        # Ajustar confianza según la tendencia
        if tendencia == 'alta':
            confianza += 0.15
        elif tendencia == 'media':
            confianza += 0.1
        elif tendencia == 'baja':
            confianza += 0.05

        # Calcular variabilidad de ventas para ajustar confianza
        if promedio_actual > 0 and promedio_anterior > 0:
            variabilidad = abs((promedio_actual - promedio_anterior) / max(promedio_actual, promedio_anterior))
            if variabilidad < 0.1:  # Ventas muy estables
                confianza += 0.15
            elif variabilidad < 0.25:  # Ventas relativamente estables
                confianza += 0.1

        # Limitar confianza a 1.0 (100%)
        confianza = min(confianza, 1.0)

        prediccion = PrediccionVenta.objects.create(
            producto=producto,
            fecha_inicio_analisis=mes_anterior,
            fecha_fin_analisis=fecha_actual,
            ventas_promedio=Decimal(str(promedio_actual)),
            tendencia=tendencia,
            confianza_prediccion=Decimal(str(confianza)),
            cantidad_sugerida=cantidad_sugerida,
            observaciones=f'Basado en ventas del último mes: {ventas_mes_actual["total_vendido"] or 0} unidades. Ingresos: ${ventas_mes_actual["total_ingresos"] or 0}'
        )
        predicciones.append(prediccion)

    # Filtrar predicciones por tendencia si se especifica
    if tendencia_filtro and tendencia_filtro != 'todas':
        predicciones = [p for p in predicciones if p.tendencia == tendencia_filtro]
    
    # Configurar paginación
    from django.core.paginator import Paginator
    paginator = Paginator(predicciones, 10)  # Mostrar 10 predicciones por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Calcular estadísticas para el resumen
    total_predicciones = len(predicciones)
    tendencias_count = {
        'alta': len([p for p in predicciones if p.tendencia == 'alta']),
        'media': len([p for p in predicciones if p.tendencia == 'media']),
        'baja': len([p for p in predicciones if p.tendencia == 'baja']),
        'riesgo': len([p for p in predicciones if p.tendencia == 'riesgo'])
    }
    
    return render(request, 'predicciones/predicciones_list.html', {
        'predicciones': page_obj,
        'page_obj': page_obj,
        'tendencia_filtro': tendencia_filtro,
        'busqueda': busqueda,
        'total_predicciones': total_predicciones,
        'tendencias_count': tendencias_count
    })

@login_required
def actualizar_estadisticas(request):
    fecha_actual = datetime.now().date()
    productos = Producto.objects.all()

    for producto in productos:
        # Obtener ventas completadas de hoy - corregido el filtro para estado completada
        ventas_hoy = VentaDetalle.objects.filter(
            producto=producto,
            venta__fecha_creacion__date=fecha_actual,
            venta__estado='completada'  # Asegurarse que solo se consideren ventas completadas
        ).aggregate(
            cantidad_total=Sum('cantidad'),
            ingreso_total=Sum('precio_total')  # Usar precio_total en lugar de calcular
        )

        # Calcular días sin venta - mejorado para considerar solo ventas completadas
        ultima_venta = VentaDetalle.objects.filter(
            producto=producto,
            venta__estado='completada',  # Solo considerar ventas completadas
            venta__fecha_creacion__date__lt=fecha_actual
        ).order_by('-venta__fecha_creacion').first()

        dias_sin_venta = 0
        if ultima_venta:
            dias_sin_venta = (fecha_actual - ultima_venta.venta.fecha_creacion.date()).days

        # Calcular rotación de inventario - mejorado para considerar solo ventas completadas
        ventas_mes = VentaDetalle.objects.filter(
            producto=producto,
            venta__estado='completada',  # Solo considerar ventas completadas
            venta__fecha_creacion__date__gte=fecha_actual - timedelta(days=30)
        ).aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0

        rotacion = 0
        if producto.cantidad_stock > 0:
            rotacion = ventas_mes / producto.cantidad_stock

        EstadisticaVenta.objects.update_or_create(
            producto=producto,
            fecha=fecha_actual,
            defaults={
                'cantidad_vendida': ventas_hoy['cantidad_total'] or 0,
                'ingreso_total': ventas_hoy['ingreso_total'] or Decimal('0.00'),
                'rotacion_inventario': Decimal(str(rotacion)),
                'dias_sin_venta': dias_sin_venta
            }
        )

    return render(request, 'predicciones/estadisticas_list.html', {
        'estadisticas': EstadisticaVenta.objects.filter(fecha=fecha_actual)
    })