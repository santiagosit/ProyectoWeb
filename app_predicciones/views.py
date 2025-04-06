from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, Avg, F, Q
from django.http import JsonResponse
from django.core.paginator import Paginator

from app_inventario.models import Producto
from app_ventas.models import Venta, VentaDetalle
from app_pedidos.models import Pedido, PedidoDetalle
from .models import PrediccionNegocio, HistorialPrediccion, PrediccionVenta, EstadisticaVenta
import json
from django.utils.safestring import mark_safe

@login_required
def dashboard_predicciones(request):
    """Vista principal del dashboard de predicciones"""
    # Contar predicciones por tipo y prioridad
    predicciones_por_tipo = PrediccionNegocio.objects.values('tipo_prediccion').annotate(
        count=Count('id')
    ).order_by('tipo_prediccion')
    
    predicciones_por_prioridad = PrediccionNegocio.objects.values('prioridad').annotate(
        count=Count('id')
    ).order_by('prioridad')
    
    # Obtener productos con oportunidades de compra de alta prioridad
    oportunidades_compra = PrediccionNegocio.objects.filter(
        tipo_prediccion='compra',
        prioridad='alta'
    ).select_related('producto')[:5]
    
    # Obtener productos con oportunidades de venta
    oportunidades_venta = PrediccionNegocio.objects.filter(
        tipo_prediccion='venta'
    ).select_related('producto')[:5]
    
    context = {
        'predicciones_por_tipo': predicciones_por_tipo,
        'predicciones_por_prioridad': predicciones_por_prioridad,
        'oportunidades_compra': oportunidades_compra,
        'oportunidades_venta': oportunidades_venta,
        'total_predicciones': PrediccionNegocio.objects.count(),
        'fecha_actualizacion': PrediccionNegocio.objects.order_by('-fecha_generacion').first().fecha_generacion if PrediccionNegocio.objects.exists() else None
    }
    
    return render(request, 'predicciones/dashboard.html', context)

@login_required
def lista_predicciones(request):
    """Vista para listar todas las predicciones con filtros"""
    # Parámetros de filtrado
    tipo = request.GET.get('tipo', '')
    prioridad = request.GET.get('prioridad', '')
    producto_id = request.GET.get('producto', '')
    
    # Construir consulta base
    predicciones = PrediccionNegocio.objects.select_related('producto').order_by('-prioridad', '-fecha_generacion')
    
    # Aplicar filtros si se proporcionan
    if tipo:
        predicciones = predicciones.filter(tipo_prediccion=tipo)
    if prioridad:
        predicciones = predicciones.filter(prioridad=prioridad)
    if producto_id:
        predicciones = predicciones.filter(producto_id=producto_id)
    
    # Paginación
    paginator = Paginator(predicciones, 15)  # 15 predicciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Datos para filtros
    productos = Producto.objects.all().order_by('nombre')
    
    context = {
        'page_obj': page_obj,
        'productos': productos,
        'tipos_prediccion': dict(PrediccionNegocio.TIPO_PREDICCION),
        'prioridades': dict(PrediccionNegocio.PRIORIDAD_CHOICES),
        'filtros': {
            'tipo': tipo,
            'prioridad': prioridad,
            'producto': producto_id
        }
    }
    
    return render(request, 'predicciones/lista_predicciones.html', context)

@login_required
def detalle_prediccion(request, prediccion_id):
    """Vista para ver detalles completos de una predicción"""
    prediccion = get_object_or_404(PrediccionNegocio, id=prediccion_id)
    
    # Obtener historial de ventas para este producto
    ventas_historicas = VentaDetalle.objects.filter(
        producto=prediccion.producto,
        venta__estado='completada'
    ).values('venta__fecha_creacion__date').annotate(
        total_unidades=Sum('cantidad'),
        total_venta=Sum('precio_total')
    ).order_by('-venta__fecha_creacion__date')[:30]
    
    # Obtener historial de pedidos para este producto
    pedidos_historicos = PedidoDetalle.objects.filter(
        producto=prediccion.producto,
        pedido__estado='recibido'
    ).values('pedido__fecha_pedido').annotate(
        total_unidades=Sum('cantidad'),
        costo_total=Sum(F('cantidad') * F('costo_unitario'))
    ).order_by('-pedido__fecha_pedido')[:10]
    
    context = {
        'prediccion': prediccion,
        'ventas_historicas': ventas_historicas,
        'pedidos_historicos': pedidos_historicos,
        'producto': prediccion.producto
    }
    
    return render(request, 'predicciones/detalle_prediccion.html', context)

@login_required
def generar_predicciones(request):
    """Vista para generar nuevas predicciones de negocio"""
    if request.method == 'POST':
        # Verificar si se solicitó análisis de todos los productos o de productos específicos
        productos_ids = request.POST.getlist('productos')
        
        if not productos_ids:
            # Si no se seleccionaron productos específicos, analizar todos
            productos = Producto.objects.all()
        else:
            productos = Producto.objects.filter(id__in=productos_ids)
        
        # Contador de predicciones generadas
        contador = 0
        
        for producto in productos:
            # Crear una nueva predicción para cada producto
            prediccion = PrediccionNegocio(producto=producto)
            prediccion.generar_prediccion()  # Este método hace todos los cálculos y guarda la predicción
            contador += 1
        
        messages.success(request, f"Se han generado {contador} predicciones de negocio.")
        return redirect('predicciones:lista_predicciones')
    
    # Si es GET, mostrar formulario para seleccionar productos
    productos = Producto.objects.all().order_by('nombre')
    context = {
        'productos': productos
    }
    
    return render(request, 'predicciones/generar_predicciones.html', context)

@login_required
def evaluar_prediccion(request, prediccion_id):
    """Vista para evaluar la precisión de una predicción pasada"""
    prediccion = get_object_or_404(PrediccionNegocio, id=prediccion_id)
    
    if request.method == 'POST':
        precision = request.POST.get('precision', 0)
        comentarios = request.POST.get('comentarios', '')
        
        # Crear historial de evaluación
        HistorialPrediccion.objects.create(
            prediccion=prediccion,
            precision=precision,
            comentarios=comentarios
        )
        
        messages.success(request, "La evaluación de la predicción ha sido registrada.")
        return redirect('predicciones:detalle_prediccion', prediccion_id=prediccion_id)
    
    context = {
        'prediccion': prediccion
    }
    
    return render(request, 'predicciones/evaluar_prediccion.html', context)

@login_required
def productos_baja_rotacion(request):
    """Vista para mostrar productos con baja rotación"""
    productos = PrediccionNegocio.objects.filter(
        rotacion_mensual__lt=0.5,
        producto__cantidad_stock__gt=0
    ).select_related('producto').order_by('rotacion_mensual')
    
    context = {
        'productos': productos,
        'titulo': 'Productos con Baja Rotación'
    }
    
    return render(request, 'predicciones/reporte_productos.html', context)

@login_required
def productos_alta_rotacion(request):
    """Vista para mostrar productos con alta rotación"""
    productos = PrediccionNegocio.objects.filter(
        rotacion_mensual__gt=1.0
    ).select_related('producto').order_by('-rotacion_mensual')
    
    context = {
        'productos': productos,
        'titulo': 'Productos con Alta Rotación'
    }
    
    return render(request, 'predicciones/reporte_productos.html', context)

@login_required
def reporte_oportunidades(request):
    """Vista para mostrar oportunidades de negocio"""
    oportunidades = PrediccionNegocio.objects.filter(
        Q(tipo_prediccion='compra') | Q(tipo_prediccion='venta')
    ).select_related('producto').order_by('-prioridad', '-fecha_generacion')
    
    context = {
        'oportunidades': oportunidades,
        'titulo': 'Oportunidades de Negocio'
    }
    
    return render(request, 'predicciones/reporte_oportunidades.html', context)

@login_required
def tendencias_producto(request, producto_id):
    """Vista para mostrar tendencias de un producto específico"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Obtener ventas históricas
    ventas_historicas = VentaDetalle.objects.filter(
        producto=producto,
        venta__estado='completada'
    ).values('venta__fecha_creacion__date').annotate(
        total_unidades=Sum('cantidad'),
        total_venta=Sum('precio_total')
    ).order_by('venta__fecha_creacion__date')
    
    # Obtener predicciones históricas
    predicciones = PrediccionNegocio.objects.filter(
        producto=producto
    ).order_by('-fecha_generacion')
    
    # Prepare data for the chart in JSON format
    ventas_labels = []
    ventas_unidades = []
    
    for venta in ventas_historicas:
        fecha = venta['venta__fecha_creacion__date']
        if hasattr(fecha, 'strftime'):
            ventas_labels.append(fecha.strftime('%d/%m/%Y'))
        else:
            ventas_labels.append(str(fecha))
        ventas_unidades.append(float(venta['total_unidades'] or 0))
    
    # If no data, provide defaults
    if not ventas_labels:
        ventas_labels = ['Sin datos']
        ventas_unidades = [0]
    
    # Create a JSON object with both arrays
    ventas_historicas_json = json.dumps({
        'labels': ventas_labels,
        'unidades': ventas_unidades
    })
    
    context = {
        'producto': producto,
        'predicciones': predicciones,
        'ventas_historicas': ventas_historicas,
        'ventas_historicas_json': mark_safe(ventas_historicas_json)
    }
    
    return render(request, 'predicciones/tendencias_producto.html', context)

@login_required
def estadisticas_list(request):
    """Vista para mostrar estadísticas de predicciones"""
    # Obtener estadísticas generales
    total_predicciones = PrediccionNegocio.objects.count()
    predicciones_por_tipo = PrediccionNegocio.objects.values('tipo_prediccion').annotate(
        count=Count('id')
    ).order_by('tipo_prediccion')
    
    predicciones_por_prioridad = PrediccionNegocio.objects.values('prioridad').annotate(
        count=Count('id')
    ).order_by('prioridad')
    
    # Productos con mayor rotación
    productos_alta_rotacion = PrediccionNegocio.objects.filter(
        rotacion_mensual__gt=1.0
    ).select_related('producto').order_by('-rotacion_mensual')[:10]
    
    # Productos con baja rotación
    productos_baja_rotacion = PrediccionNegocio.objects.filter(
        rotacion_mensual__lt=0.5,
        producto__cantidad_stock__gt=0
    ).select_related('producto').order_by('rotacion_mensual')[:10]
    
    # Productos con mejor margen
    productos_mejor_margen = PrediccionNegocio.objects.select_related('producto').order_by('-margen_actual')[:10]
    
    context = {
        'total_predicciones': total_predicciones,
        'predicciones_por_tipo': predicciones_por_tipo,
        'predicciones_por_prioridad': predicciones_por_prioridad,
        'productos_alta_rotacion': productos_alta_rotacion,
        'productos_baja_rotacion': productos_baja_rotacion,
        'productos_mejor_margen': productos_mejor_margen,
    }
    
    return render(request, 'predicciones/estadisticas.html', context)


@login_required
def datos_predicciones_api(request):
    """API para obtener datos de predicciones para gráficos"""
    # Contar predicciones por tipo
    predicciones_por_tipo = PrediccionNegocio.objects.values('tipo_prediccion').annotate(
        count=Count('id')
    ).order_by('tipo_prediccion')
    
    # Contar predicciones por prioridad
    predicciones_por_prioridad = PrediccionNegocio.objects.values('prioridad').annotate(
        count=Count('id')
    ).order_by('prioridad')
    
    # Formatear datos para la API
    datos_tipo = {
        'labels': [tipo['tipo_prediccion'].title() for tipo in predicciones_por_tipo],
        'values': [tipo['count'] for tipo in predicciones_por_tipo]
    }
    
    datos_prioridad = {
        'labels': [prioridad['prioridad'].title() for prioridad in predicciones_por_prioridad],
        'values': [prioridad['count'] for prioridad in predicciones_por_prioridad]
    }
    
    # Devolver datos en formato JSON
    return JsonResponse({
        'tipo': datos_tipo,
        'prioridad': datos_prioridad
    })