from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta, datetime, date
from django.db.models import Sum, Avg, Count, F, Q
from django.db.models.functions import TruncWeek, TruncMonth
from app_inventario.models import Producto
from app_ventas.models import VentaDetalle
from app_pedidos.models import Pedido, PedidoDetalle
import json
from collections import defaultdict
import calendar
import numpy as np
from sklearn.linear_model import LinearRegression  # Para regresión lineal
from app_usuarios.utils import is_admin_or_superuser

@login_required
@user_passes_test(is_admin_or_superuser, login_url='empleado_dashboard')
def oportunidad_compra_prediccion(request):
    hoy = timezone.now()
    hace_3_anios = hoy - timedelta(days=365*3)
    productos = Producto.objects.all()
    producto_id = request.GET.get('producto')
    producto_seleccionado = None
    labels = []
    data_historico = []
    data_prediccion = []
    promedio_historico = []
    oportunidad_indices = []
    mejor_mes = None
    mejor_precio = None

    if producto_id:
        try:
            producto_seleccionado = Producto.objects.get(id=producto_id)
            detalles = PedidoDetalle.objects.filter(
                producto=producto_seleccionado,
                pedido__estado='recibido',
                pedido__fecha_pedido__gte=hace_3_anios
            ).order_by('pedido__fecha_pedido')
            # Agrupar por mes y calcular el precio promedio mensual
            precios_por_mes = {}
            cantidades_por_mes = {}
            for det in detalles:
                mes = det.pedido.fecha_pedido.strftime('%Y-%m')
                if mes not in precios_por_mes:
                    precios_por_mes[mes] = 0
                    cantidades_por_mes[mes] = 0
                precios_por_mes[mes] += float(det.costo_unitario) * det.cantidad
                cantidades_por_mes[mes] += det.cantidad
            # Calcular promedio mensual
            meses_ordenados = sorted(precios_por_mes.keys())
            precios_historicos = []
            for mes in meses_ordenados:
                if cantidades_por_mes[mes] > 0:
                    labels.append(mes)
                    precio_mes = round(precios_por_mes[mes] / cantidades_por_mes[mes], 2)
                    data_historico.append(precio_mes)
                    precios_historicos.append(precio_mes)
            # Calcular umbral de oportunidad (percentil 25 de precios históricos)
            if precios_historicos:
                import numpy as np
                percentil_25 = np.percentile(precios_historicos, 25)
                for idx, precio in enumerate(data_historico):
                    if precio <= percentil_25 or any(abs(precio - p) / p < 0.05 for p in precios_historicos if p <= percentil_25):
                        oportunidad_indices.append(idx)
            # Predicción de precios futuros (próximos 6 meses)
            meses_futuros = 6
            if len(data_historico) > 1:
                import numpy as np
                from sklearn.linear_model import LinearRegression
                x = np.arange(len(data_historico)).reshape(-1, 1)
                y = np.array(data_historico)
                model = LinearRegression()
                model.fit(x, y)
                for i in range(len(data_historico), len(data_historico) + meses_futuros):
                    pred = float(model.predict(np.array([[i]])))
                    data_prediccion.append(round(pred, 2))
                    # Calcular el siguiente mes
                    last_month = datetime.strptime(meses_ordenados[-1], '%Y-%m')
                    next_month = (last_month.month + (i - len(data_historico) + 1) - 1) % 12 + 1
                    next_year = last_month.year + ((last_month.month + (i - len(data_historico) + 1) - 1) // 12)
                    labels.append(f"{next_year}-{next_month:02d}")
            elif len(data_historico) == 1:
                for i in range(meses_futuros):
                    data_prediccion.append(data_historico[0])
                    last_month = datetime.strptime(meses_ordenados[-1], '%Y-%m')
                    next_month = (last_month.month + (i + 1) - 1) % 12 + 1
                    next_year = last_month.year + ((last_month.month + (i + 1) - 1) // 12)
                    labels.append(f"{next_year}-{next_month:02d}")
            # Calcular promedio histórico para la línea de referencia
            if data_historico:
                prom = round(sum(data_historico) / len(data_historico), 2)
                promedio_historico = [prom] * (len(data_historico) + len(data_prediccion))
            # Recomendar el mejor mes para comprar (menor precio futuro)
            if data_prediccion:
                mejor_precio = min(data_prediccion)
                mejor_idx = data_prediccion.index(mejor_precio)
                mejor_mes = labels[len(data_historico) + mejor_idx] if len(labels) > len(data_historico) + mejor_idx else None
        except Producto.DoesNotExist:
            producto_seleccionado = None
    context = {
        'productos': productos,
        'producto_seleccionado': producto_seleccionado,
        'labels': json.dumps(labels),
        'data_historico': json.dumps(data_historico),
        'data_prediccion': json.dumps([None]*len(data_historico) + data_prediccion),  # Predicción solo en meses futuros
        'promedio_historico': json.dumps(promedio_historico),
        'oportunidad_indices': json.dumps(oportunidad_indices),
    }
    return render(request, 'predicciones/oportunidad_compra.html', context)

@login_required
@user_passes_test(is_admin_or_superuser, login_url='empleado_dashboard')
def dashboard_predicciones(request):
    # Configuración de fechas
    hoy = timezone.now()
    hace_6_meses = hoy - timedelta(days=180)  # 6 meses en lugar de 3
    hace_4_semanas = hoy - timedelta(weeks=4)
    proximo_mes = hoy + timedelta(days=30)
    
    # Obtener todos los productos y verificar que existan
    productos = Producto.objects.all()
    print(f"Cantidad de productos encontrados: {productos.count()}")
    if productos.count() == 0:
        print("ADVERTENCIA: No hay productos en la base de datos")
        # Crear productos de prueba si no hay productos en la base de datos
        productos_prueba = [
            {"nombre": "Producto de Prueba 1", "descripcion": "Descripción de prueba 1", "precio": 10.50, "cantidad_stock": 15, "stock_minimo": 5},
            {"nombre": "Producto de Prueba 2", "descripcion": "Descripción de prueba 2", "precio": 20.75, "cantidad_stock": 8, "stock_minimo": 3},
        ]
        
        for prod_data in productos_prueba:
            try:
                Producto.objects.create(**prod_data)
                print(f"Producto creado: {prod_data['nombre']}")
            except Exception as e:
                print(f"Error al crear producto: {e}")
        
        # Volver a cargar los productos
        productos = Producto.objects.all()
        print(f"Productos después de crear productos de prueba: {productos.count()}")
    
    # Obtener producto seleccionado (por GET)
    producto_id = request.GET.get('producto')
    producto_seleccionado = None
    ventas_producto = []
    labels = []
    data = []
    if producto_id:
        try:
            producto_seleccionado = Producto.objects.get(id=producto_id)
            ventas = VentaDetalle.objects.filter(
                producto=producto_seleccionado,
                venta__estado='completada',
                venta__fecha_creacion__gte=hace_6_meses
            ).order_by('venta__fecha_creacion')
            # Agrupar por semana o mes
            ventas_por_mes = {}
            for v in ventas:
                mes = v.venta.fecha_creacion.strftime('%Y-%m')
                ventas_por_mes.setdefault(mes, 0)
                ventas_por_mes[mes] += v.cantidad
            labels = list(ventas_por_mes.keys())
            data = list(ventas_por_mes.values())
            ventas_producto = ventas

            # --- PREDICCIÓN DE OPORTUNIDAD DE PEDIDO ---
            # Promedio mensual de ventas
            meses_ventas = len(ventas_por_mes)
            promedio_mensual = sum(ventas_por_mes.values()) / meses_ventas if meses_ventas else 0
            stock_actual = producto_seleccionado.cantidad_stock
            stock_minimo = producto_seleccionado.stock_minimo
            demanda_proyectada = round(promedio_mensual)

            # Detectar temporada alta (ejemplo: diciembre, junio)
            mes_actual = hoy.month
            temporada_alta = mes_actual in [6, 12]  # Puedes ajustar según tu negocio
            factor_temporada = 1.3 if temporada_alta else 1.0
            demanda_ajustada = int(demanda_proyectada * factor_temporada)

            # Calcular cuándo pedir (si stock < demanda proyectada + stock mínimo)
            necesita_pedido = stock_actual < (demanda_ajustada + stock_minimo)
            if necesita_pedido:
                fecha_sugerida = hoy.strftime('%Y-%m-%d')
                urgencia = 'Alta'
            else:
                # Calcular semanas de cobertura
                semanas_cobertura = (stock_actual - stock_minimo) / (demanda_ajustada / 4) if demanda_ajustada else 99
                dias_hasta_pedido = max(0, int((semanas_cobertura - 1) * 7))
                fecha_sugerida = (hoy + timedelta(days=dias_hasta_pedido)).strftime('%Y-%m-%d')
                urgencia = 'Media' if semanas_cobertura < 4 else 'Baja'
            cantidad_sugerida = max(0, demanda_ajustada + stock_minimo - stock_actual)
        except Producto.DoesNotExist:
            producto_seleccionado = None
            demanda_proyectada = 0
            fecha_sugerida = None
            cantidad_sugerida = 0
            urgencia = None
    else:
        demanda_proyectada = 0
        fecha_sugerida = None
        cantidad_sugerida = 0
        urgencia = None

    context = {
        'productos': productos,
        'producto_seleccionado': producto_seleccionado,
        'labels': labels,
        'data': data,
        'ventas_producto': ventas_producto,
        'fecha_analisis': hoy.strftime('%Y-%m-%d'),
        'periodo_analisis': hace_6_meses.strftime('%Y-%m-%d'),
        'demanda_proyectada': demanda_proyectada,
        'fecha_sugerida': fecha_sugerida,
        'cantidad_sugerida': cantidad_sugerida,
        'urgencia': urgencia,
        'temporada_alta': temporada_alta if producto_id else False,
    }
    return render(request, 'predicciones/dashboard.html', context)
    # Agrupar ventas por producto y mes
    ventas_mensuales_por_producto = defaultdict(lambda: defaultdict(int))  # {producto: {mes: total}}
    meses_labels = set()
    
    for detalle in ventas_mensuales:
        producto = detalle.producto.nombre
        mes = detalle.mes.strftime('%Y-%m')
        ventas_mensuales_por_producto[producto][mes] += detalle.cantidad
        meses_labels.add(mes)
    
    meses_labels = sorted(list(meses_labels))
    
    # Calcular próximas 4 semanas (para predicción)
    ultima_semana = datetime.strptime(semanas_labels[-1], '%Y-%m-%d').date() if semanas_labels else hoy.date()
    proximas_semanas = []
    for i in range(1, 5):  # Próximas 4 semanas
        proxima = (ultima_semana + timedelta(days=7*i)).strftime('%Y-%m-%d')
        proximas_semanas.append(proxima)
    
    # Calcular próximos 2 meses (para predicción)
    ultimo_mes = datetime.strptime(meses_labels[-1], '%Y-%m').date() if meses_labels else hoy.date().replace(day=1)
    proximos_meses = []
    for i in range(1, 3):  # Próximos 2 meses
        # Avanzar al próximo mes
        if ultimo_mes.month == 12:
            proximo = date(ultimo_mes.year + 1, 1, 1)
        else:
            proximo = date(ultimo_mes.year, ultimo_mes.month + i, 1)
        proximos_meses.append(proximo.strftime('%Y-%m'))
    
    # Cálculo de predicción y oportunidades de pedido
    tendencia_predicciones = {}
    oportunidades_pedido = []
    
    for producto_obj in productos:
        producto_nombre = producto_obj.nombre
        datos_semanales = [ventas_por_producto[producto_nombre].get(sem, 0) for sem in semanas_labels]
        datos_mensuales = [ventas_mensuales_por_producto[producto_nombre].get(mes, 0) for mes in meses_labels]
        
        # Predicción semanal usando regresión lineal
        predicciones_semanales = []
        if len(datos_semanales) > 1:
            # Regresión lineal para datos semanales
            x = np.array(range(len(datos_semanales)))
            y = np.array(datos_semanales)
            if len(x) > 0 and len(y) > 0:  # Verificar que hay datos
                # Calcular coeficientes de regresión
                n = len(x)
                x_mean = np.mean(x)
                y_mean = np.mean(y)
                numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
                denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
                slope = numerator / denominator if denominator != 0 else 0
                intercept = y_mean - slope * x_mean
                
                # Predecir próximas 4 semanas
                for i in range(len(datos_semanales), len(datos_semanales) + 4):
                    prediccion = max(0, round(slope * i + intercept))
                    predicciones_semanales.append(prediccion)
        
        # Si no hay suficientes datos, usar el promedio o un valor por defecto
        if not predicciones_semanales:
            promedio = sum(datos_semanales) / len(datos_semanales) if datos_semanales else 0
            predicciones_semanales = [round(promedio)] * 4
        
        # Predicción mensual
        prediccion_mensual = sum(predicciones_semanales)
        
        # Calcular si se necesita hacer un pedido
        stock_actual = producto_obj.cantidad_stock
        stock_minimo = producto_obj.stock_minimo
        demanda_proyectada = prediccion_mensual
        
        # Determinar si se necesita hacer un pedido y cuándo
        necesita_pedido = stock_actual < (demanda_proyectada + stock_minimo)
        semanas_hasta_pedido = 0
        
        if necesita_pedido:
            # Calcular cuántas semanas aguantará el stock actual
            stock_restante = stock_actual
            for i, pred_semanal in enumerate(predicciones_semanales):
                if stock_restante <= (pred_semanal + stock_minimo):
                    semanas_hasta_pedido = i
                    break
                stock_restante -= pred_semanal
            
            # Si el stock aguanta más de 4 semanas
            if semanas_hasta_pedido == 0 and stock_restante > stock_minimo:
                semanas_hasta_pedido = 4
        
        # Calcular fecha sugerida de pedido
        fecha_pedido = None
        if necesita_pedido:
            if semanas_hasta_pedido == 0:
                fecha_pedido = "Inmediato"
            else:
                dias_hasta_pedido = semanas_hasta_pedido * 7
                fecha_pedido = (hoy + timedelta(days=dias_hasta_pedido)).strftime('%Y-%m-%d')
        
        # Cantidad sugerida para el pedido (demanda proyectada + margen de seguridad - stock actual)
        margen_seguridad = max(stock_minimo, round(demanda_proyectada * 0.2))  # 20% de margen o stock mínimo
        cantidad_sugerida = max(0, demanda_proyectada + margen_seguridad - stock_actual)
        
        # Añadir a las oportunidades de pedido si se necesita pedir
        if necesita_pedido and cantidad_sugerida > 0:
            oportunidades_pedido.append({
                'producto': producto_nombre,
                'stock_actual': stock_actual,
                'stock_minimo': stock_minimo,
                'demanda_proyectada': demanda_proyectada,
                'cantidad_sugerida': cantidad_sugerida,
                'fecha_sugerida': fecha_pedido,
                'urgencia': 'Alta' if semanas_hasta_pedido == 0 else ('Media' if semanas_hasta_pedido <= 2 else 'Baja')
            })
        
        # Guardar datos para la gráfica
        tendencia_predicciones[producto_nombre] = {
            'labels': semanas_labels + proximas_semanas,
            'data': datos_semanales + predicciones_semanales,
            'prediccion_mensual': prediccion_mensual,
            'historico': datos_semanales,
            'prediccion': predicciones_semanales,
            'meses': meses_labels + proximos_meses,
            'datos_mensuales': datos_mensuales + [prediccion_mensual, prediccion_mensual],
        }
    
    # Ordenar oportunidades de pedido por urgencia
    orden_urgencia = {'Alta': 0, 'Media': 1, 'Baja': 2}
    oportunidades_pedido.sort(key=lambda x: (orden_urgencia[x['urgencia']], -x['cantidad_sugerida']))
    
    # --- SUGERENCIAS PARA TABLAS (mejorada) ---
    # Cálculo de predicción y oportunidades de pedido
    tendencia_predicciones = {}
    oportunidades_pedido = []
    
    for producto_obj in productos:
        producto_nombre = producto_obj.nombre
        datos_semanales = [ventas_por_producto[producto_nombre].get(sem, 0) for sem in semanas_labels]
        datos_mensuales = [ventas_mensuales_por_producto[producto_nombre].get(mes, 0) for mes in meses_labels]
        
        # Predicción semanal usando regresión lineal
        predicciones_semanales = []
        if len(datos_semanales) > 1:
            # Regresión lineal para datos semanales
            x = np.array(range(len(datos_semanales)))
            y = np.array(datos_semanales)
            if len(x) > 0 and len(y) > 0:  # Verificar que hay datos
                # Calcular coeficientes de regresión
                n = len(x)
                x_mean = np.mean(x)
                y_mean = np.mean(y)
                numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
                denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
                slope = numerator / denominator if denominator != 0 else 0
                intercept = y_mean - slope * x_mean
                
                # Predecir próximas 4 semanas
                for i in range(len(datos_semanales), len(datos_semanales) + 4):
                    prediccion = max(0, round(slope * i + intercept))
                    predicciones_semanales.append(prediccion)
        
        # Si no hay suficientes datos, usar el promedio o un valor por defecto
        if not predicciones_semanales:
            promedio = sum(datos_semanales) / len(datos_semanales) if datos_semanales else 0
            predicciones_semanales = [round(promedio)] * 4
        
        # Predicción mensual
        prediccion_mensual = sum(predicciones_semanales)
        
        # Calcular si se necesita hacer un pedido
        stock_actual = producto_obj.cantidad_stock
        stock_minimo = producto_obj.stock_minimo
        demanda_proyectada = prediccion_mensual
        
        # Determinar si se necesita hacer un pedido y cuándo
        necesita_pedido = stock_actual < (demanda_proyectada + stock_minimo)
        semanas_hasta_pedido = 0
        
        if necesita_pedido:
            # Calcular cuántas semanas aguantará el stock actual
            stock_restante = stock_actual
            for i, pred_semanal in enumerate(predicciones_semanales):
                if stock_restante <= (pred_semanal + stock_minimo):
                    semanas_hasta_pedido = i
                    break
                stock_restante -= pred_semanal
            
            # Si el stock aguanta más de 4 semanas
            if semanas_hasta_pedido == 0 and stock_restante > stock_minimo:
                semanas_hasta_pedido = 4
        
        # Calcular fecha sugerida de pedido
        fecha_pedido = None
        if necesita_pedido:
            if semanas_hasta_pedido == 0:
                fecha_pedido = "Inmediato"
            else:
                dias_hasta_pedido = semanas_hasta_pedido * 7
                fecha_pedido = (hoy + timedelta(days=dias_hasta_pedido)).strftime('%Y-%m-%d')
        
        # Cantidad sugerida para el pedido (demanda proyectada + margen de seguridad - stock actual)
        margen_seguridad = max(stock_minimo, round(demanda_proyectada * 0.2))  # 20% de margen o stock mínimo
        cantidad_sugerida = max(0, demanda_proyectada + margen_seguridad - stock_actual)
        
        # Añadir a las oportunidades de pedido si se necesita pedir
        if necesita_pedido and cantidad_sugerida > 0:
            oportunidades_pedido.append({
                'producto': producto_nombre,
                'stock_actual': stock_actual,
                'stock_minimo': stock_minimo,
                'demanda_proyectada': demanda_proyectada,
                'cantidad_sugerida': cantidad_sugerida,
                'fecha_sugerida': fecha_pedido,
                'urgencia': 'Alta' if semanas_hasta_pedido == 0 else ('Media' if semanas_hasta_pedido <= 2 else 'Baja')
            })
        
        # Guardar datos para la gráfica
        tendencia_predicciones[producto_nombre] = {
            'labels': semanas_labels + proximas_semanas,
            'data': datos_semanales + predicciones_semanales,
            'prediccion_mensual': prediccion_mensual,
            'historico': datos_semanales,
            'prediccion': predicciones_semanales,
            'meses': meses_labels + proximos_meses,
            'datos_mensuales': datos_mensuales + [prediccion_mensual, prediccion_mensual],
        }
    
    # Ordenar oportunidades de pedido por urgencia
    orden_urgencia = {'Alta': 0, 'Media': 1, 'Baja': 2}
    oportunidades_pedido.sort(key=lambda x: (orden_urgencia[x['urgencia']], -x['cantidad_sugerida']))
    
    # --- DEPURACIÓN Y FORZAR PRODUCTOS EN EL JSON ---
    print("\n--- DEPURACIÓN DASHBOARD PREDICCIONES ---")
    productos_all = Producto.objects.all()
    print(f"Productos encontrados: {productos_all.count()}")
    for p in productos_all:
        print(f"Producto: {p.id} - {p.nombre}")
        ventas = VentaDetalle.objects.filter(producto=p, venta__estado='completada')
        print(f"  Ventas asociadas: {ventas.count()}")
        for v in ventas:
            print(f"    VentaDetalle: VentaID={v.venta.id}, Fecha={v.venta.fecha_creacion}, Cantidad={v.cantidad}")
    print(f"Tendencia predicciones keys antes de forzar: {list(tendencia_predicciones.keys())}")

    # Forzar que todos los productos aparezcan en el JSON (aunque sea con datos vacíos)
    for p in productos_all:
        if p.nombre not in tendencia_predicciones:
            tendencia_predicciones[p.nombre] = {
                "labels": [],
                "data": [],
                "historico": [],
                "prediccion": [],
                "prediccion_mensual": 0,
                "meses": [],
                "datos_mensuales": []
            }
    print(f"Tendencia predicciones keys después de forzar: {list(tendencia_predicciones.keys())}")
    tendencia_predicciones_json = json.dumps(tendencia_predicciones)
    print(f"Datos JSON generados con {len(tendencia_predicciones)} productos")
    
    sin_productos_reales = (Producto.objects.count() == 0)
    context = {
        'tendencia_predicciones_json': tendencia_predicciones_json,
        'oportunidades_pedido': oportunidades_pedido,
        'fecha_analisis': hoy.strftime('%Y-%m-%d'),
        'periodo_analisis': hace_6_meses.strftime('%Y-%m-%d'),
        'prediccion_hasta': proximo_mes.strftime('%Y-%m-%d'),
        'sin_productos_reales': sin_productos_reales,
    }
    return render(request, 'predicciones/dashboard.html', context)
