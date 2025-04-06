from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models import Avg, Sum, Count

from app_inventario.models import Producto
from app_ventas.models import Venta, VentaDetalle
from app_pedidos.models import Pedido, PedidoDetalle
from app_finanzas.models import Ingreso, Egreso

class PrediccionNegocio(models.Model):
    TIPO_PREDICCION = [
        ('venta', 'Oportunidad de Venta'),
        ('compra', 'Oportunidad de Compra'),
        ('precio', 'Ajuste de Precio'),
        ('stock', 'Optimización de Stock')
    ]
    
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja')
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='predicciones_negocio')
    fecha_generacion = models.DateTimeField(default=timezone.now)
    tipo_prediccion = models.CharField(max_length=20, choices=TIPO_PREDICCION)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES)
    
    # Métricas calculadas
    ventas_ultimos_30_dias = models.PositiveIntegerField(default=0)
    ventas_ultimos_90_dias = models.PositiveIntegerField(default=0)
    rotacion_mensual = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    margen_actual = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    dias_stock_actual = models.PositiveIntegerField(default=0)
    
    # Recomendaciones
    cantidad_recomendada = models.PositiveIntegerField(default=0)
    precio_recomendado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_accion_recomendada = models.DateField(default=timezone.now)
    
    # Proyecciones financieras
    inversion_estimada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ganancia_estimada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    roi_estimado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Análisis detallado
    analisis = models.TextField()
    
    class Meta:
        ordering = ['-fecha_generacion', 'prioridad']
        verbose_name = 'Predicción de Negocio'
        verbose_name_plural = 'Predicciones de Negocio'
    
    def __str__(self):
        return f"{self.get_tipo_prediccion_display()} - {self.producto.nombre} - {self.get_prioridad_display()}"
    
    def calcular_metricas(self):
        """Calcula las métricas basadas en los datos históricos"""
        hoy = timezone.now().date()
        hace_30_dias = hoy - timezone.timedelta(days=30)
        hace_90_dias = hoy - timezone.timedelta(days=90)
        
        # Calcular ventas recientes
        ventas_30 = VentaDetalle.objects.filter(
            producto=self.producto,
            venta__estado='completada',
            venta__fecha_creacion__date__gte=hace_30_dias
        ).aggregate(
            total_unidades=Sum('cantidad'),
            total_ventas=Sum('precio_total')
        )
        
        ventas_90 = VentaDetalle.objects.filter(
            producto=self.producto,
            venta__estado='completada',
            venta__fecha_creacion__date__gte=hace_90_dias
        ).aggregate(
            total_unidades=Sum('cantidad'),
            total_ventas=Sum('precio_total')
        )
        
        # Calcular el costo promedio de compra
        costo_promedio = PedidoDetalle.objects.filter(
            producto=self.producto,
            pedido__estado='recibido',
            pedido__fecha_pedido__gte=hace_90_dias
        ).aggregate(
            costo_prom=Avg('costo_unitario')
        )['costo_prom'] or self.producto.precio * Decimal('0.6')  # Estimación si no hay datos
        
        # Actualizar métricas
        self.ventas_ultimos_30_dias = ventas_30['total_unidades'] or 0
        self.ventas_ultimos_90_dias = ventas_90['total_unidades'] or 0
        
        # Calcular rotación mensual (ventas mensuales / stock actual)
        ventas_mensuales = self.ventas_ultimos_30_dias
        if ventas_mensuales > 0 and self.producto.cantidad_stock > 0:
            self.rotacion_mensual = round(ventas_mensuales / self.producto.cantidad_stock, 2)
            self.dias_stock_actual = round((self.producto.cantidad_stock / ventas_mensuales) * 30)
        else:
            self.rotacion_mensual = Decimal('0.00')
            self.dias_stock_actual = 999 if self.producto.cantidad_stock > 0 else 0  # Valor alto si hay stock pero no ventas
        
        # Calcular margen actual
        if costo_promedio and costo_promedio > 0:
            self.margen_actual = round((self.producto.precio - costo_promedio) / self.producto.precio * 100, 2)
        
    def generar_prediccion(self):
        """Analiza datos y genera recomendaciones de negocio"""
        self.calcular_metricas()
        
        # Decisiones basadas en datos
        stock_min = self.producto.stock_minimo
        stock_actual = self.producto.cantidad_stock
        ventas_recientes = self.ventas_ultimos_30_dias
        
        # Determinar tipo de oportunidad
        if stock_actual <= stock_min:
            # Oportunidad de compra por stock bajo
            self.tipo_prediccion = 'compra'
            self.prioridad = 'alta'
            self.cantidad_recomendada = max(stock_min * 3, ventas_recientes * 2)
            self.fecha_accion_recomendada = timezone.now().date()
            
            # Cálculos financieros
            costo_estimado = self.producto.precio * Decimal('0.6')  # Estimación de costo 
            self.inversion_estimada = costo_estimado * self.cantidad_recomendada
            self.ganancia_estimada = (self.producto.precio - costo_estimado) * self.cantidad_recomendada
            self.roi_estimado = (self.ganancia_estimada / self.inversion_estimada * 100) if self.inversion_estimada else Decimal('0')
            
            self.analisis = f"Stock crítico: {stock_actual} unidades disponibles (mínimo: {stock_min}). " \
                            f"Con ventas de {ventas_recientes} unidades en los últimos 30 días, se recomienda " \
                            f"realizar un pedido inmediato de {self.cantidad_recomendada} unidades para evitar " \
                            f"pérdidas de ventas. La inversión estimada de ${self.inversion_estimada} generaría " \
                            f"una ganancia potencial de ${self.ganancia_estimada} (ROI: {self.roi_estimado}%)."
        
        elif self.rotacion_mensual > Decimal('2.0'):
            # Producto de alta rotación: oportunidad de venta
            self.tipo_prediccion = 'venta'
            self.prioridad = 'media'
            self.analisis = f"Producto de alta rotación ({self.rotacion_mensual} veces por mes). " \
                             f"Margen actual: {self.margen_actual}%. Considerar promoción para aumentar volumen " \
                             f"de ventas o evaluar incremento de precio en {round(self.margen_actual * 0.1, 2)}% " \
                             f"para maximizar ganancias manteniendo la demanda."
        
        elif self.rotacion_mensual < Decimal('0.5') and stock_actual > stock_min * 2:
            # Producto estancado: ajuste de precio
            self.tipo_prediccion = 'precio'
            self.prioridad = 'media'
            descuento_sugerido = 10 if self.margen_actual > 30 else 5
            self.precio_recomendado = self.producto.precio * (1 - Decimal(descuento_sugerido) / 100)
            self.fecha_accion_recomendada = timezone.now().date() + timezone.timedelta(days=7)
            
            self.analisis = f"Baja rotación ({self.rotacion_mensual}) con stock elevado ({stock_actual} unidades). " \
                            f"Se recomienda promoción con {descuento_sugerido}% de descuento (nuevo precio: ${self.precio_recomendado}) " \
                            f"para mejorar liquidez e incrementar rotación."
        
        elif self.dias_stock_actual > 60 and self.dias_stock_actual < 120:
            # Optimización de stock
            self.tipo_prediccion = 'stock'
            self.prioridad = 'baja'
            self.analisis = f"Stock para {self.dias_stock_actual} días al ritmo actual de ventas. " \
                            f"Considerar no reponer existencias hasta reducir inventario. " \
                            f"Capital inmovilizado estimado: ${stock_actual * self.producto.precio * Decimal('0.6')}."
        
        else:
            # Producto en equilibrio
            self.tipo_prediccion = 'stock'
            self.prioridad = 'baja'
            self.analisis = f"Producto con indicadores equilibrados. Rotación: {self.rotacion_mensual}. " \
                            f"Días de stock: {self.dias_stock_actual}. Margen: {self.margen_actual}%. " \
                            f"Mantener estrategia actual y monitorear semanalmente."
        
        self.save()
        return self
        
    def save(self, *args, **kwargs):
        if not self.pk:  # Solo para nuevos registros
            self.calcular_metricas()
        super().save(*args, **kwargs)


class HistorialPrediccion(models.Model):
    """Guarda historial de predicciones para análisis de precisión"""
    prediccion = models.ForeignKey(PrediccionNegocio, on_delete=models.CASCADE, related_name='historial')
    fecha_evaluacion = models.DateTimeField(default=timezone.now)
    precision = models.DecimalField(max_digits=5, decimal_places=2)
    comentarios = models.TextField()
    
    def __str__(self):
        return f"Evaluación de predicción #{self.prediccion.id} - {self.precision}%"

# Nuevos modelos que faltan
class PrediccionVenta(models.Model):
    """Modelo para predecir ventas futuras de productos"""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='predicciones_venta')
    fecha_generacion = models.DateTimeField(default=timezone.now)
    periodo_prediccion = models.CharField(max_length=20, choices=[
        ('semanal', 'Próxima Semana'),
        ('mensual', 'Próximo Mes'),
        ('trimestral', 'Próximo Trimestre')
    ])
    
    # Valores de predicción
    unidades_estimadas = models.PositiveIntegerField()
    ingresos_estimados = models.DecimalField(max_digits=10, decimal_places=2)
    confianza_prediccion = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de confianza")
    
    # Factores de influencia
    factores_considerados = models.TextField(help_text="Factores que influyen en la predicción")
    
    class Meta:
        ordering = ['-fecha_generacion']
        verbose_name = 'Predicción de Venta'
        verbose_name_plural = 'Predicciones de Venta'
    
    def __str__(self):
        return f"Predicción {self.get_periodo_prediccion_display()} - {self.producto.nombre}"
    
    def calcular_prediccion(self):
        """Calcula la predicción de ventas basada en datos históricos"""
        hoy = timezone.now().date()
        
        # Definir periodos para análisis
        if self.periodo_prediccion == 'semanal':
            dias_analisis = 60  # Analizar últimos 60 días para predecir semana
            factor_periodo = 7  # Una semana
        elif self.periodo_prediccion == 'mensual':
            dias_analisis = 180  # Analizar últimos 180 días para predecir mes
            factor_periodo = 30  # Un mes
        else:  # trimestral
            dias_analisis = 365  # Analizar último año para predecir trimestre
            factor_periodo = 90  # Un trimestre
        
        fecha_inicio = hoy - timezone.timedelta(days=dias_analisis)
        
        # Obtener datos históricos de ventas
        ventas_historicas = VentaDetalle.objects.filter(
            producto=self.producto,
            venta__estado='completada',
            venta__fecha_creacion__date__gte=fecha_inicio
        ).values('venta__fecha_creacion__date').annotate(
            unidades=Sum('cantidad'),
            ingresos=Sum('precio_total')
        ).order_by('venta__fecha_creacion__date')
        
        # Calcular promedios para la predicción
        if ventas_historicas:
            total_unidades = sum(v['unidades'] for v in ventas_historicas)
            total_ingresos = sum(v['ingresos'] for v in ventas_historicas)
            dias_con_datos = len(ventas_historicas)
            
            # Calcular promedio diario y proyectar al periodo
            if dias_con_datos > 0:
                promedio_unidades_diario = total_unidades / dias_analisis
                promedio_ingresos_diario = total_ingresos / dias_analisis
                
                # Proyectar al periodo futuro
                self.unidades_estimadas = round(promedio_unidades_diario * factor_periodo)
                self.ingresos_estimados = round(promedio_ingresos_diario * factor_periodo, 2)
                
                # Calcular confianza basada en la consistencia de datos
                # Más días con ventas = mayor confianza
                self.confianza_prediccion = min(90, (dias_con_datos / dias_analisis) * 100)
                
                # Factores considerados
                self.factores_considerados = (
                    f"Análisis basado en {dias_con_datos} días con ventas de los últimos {dias_analisis} días. "
                    f"Promedio diario: {promedio_unidades_diario:.2f} unidades, ${promedio_ingresos_diario:.2f}. "
                    f"Proyección ajustada al periodo de {factor_periodo} días."
                )
            else:
                # No hay suficientes datos
                self.unidades_estimadas = 0
                self.ingresos_estimados = Decimal('0.00')
                self.confianza_prediccion = Decimal('0.00')
                self.factores_considerados = "Datos históricos insuficientes para una predicción confiable."
        else:
            # No hay datos históricos
            self.unidades_estimadas = 0
            self.ingresos_estimados = Decimal('0.00')
            self.confianza_prediccion = Decimal('0.00')
            self.factores_considerados = "Sin datos históricos de ventas para este producto."
        
        self.save()
        return self
    
    def save(self, *args, **kwargs):
        if not self.pk and not hasattr(self, '_skip_calculation'):
            self._skip_calculation = True
            self.calcular_prediccion()
        super().save(*args, **kwargs)


class EstadisticaVenta(models.Model):
    """Modelo para almacenar estadísticas de ventas por producto y periodo"""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='estadisticas_venta')
    periodo = models.CharField(max_length=20, choices=[
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('anual', 'Anual')
    ])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    # Métricas de ventas
    unidades_vendidas = models.PositiveIntegerField(default=0)
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_promedio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Métricas de tendencia
    variacion_periodo_anterior = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, 
                                                    help_text="Porcentaje de variación respecto al periodo anterior")
    tendencia = models.CharField(max_length=20, choices=[
        ('crecimiento', 'Crecimiento'),
        ('estable', 'Estable'),
        ('decrecimiento', 'Decrecimiento')
    ], null=True, blank=True)
    
    class Meta:
        unique_together = ['producto', 'periodo', 'fecha_inicio']
        ordering = ['-fecha_inicio', 'producto']
        verbose_name = 'Estadística de Venta'
        verbose_name_plural = 'Estadísticas de Venta'
    
    def __str__(self):
        return f"Estadística {self.get_periodo_display()} - {self.producto.nombre} ({self.fecha_inicio} a {self.fecha_fin})"
    
    def calcular_estadisticas(self):
        """Calcula las estadísticas de ventas para el periodo especificado"""
        # Obtener ventas del periodo actual
        ventas_periodo = VentaDetalle.objects.filter(
            producto=self.producto,
            venta__estado='completada',
            venta__fecha_creacion__date__gte=self.fecha_inicio,
            venta__fecha_creacion__date__lte=self.fecha_fin
        ).aggregate(
            total_unidades=Sum('cantidad'),
            total_ingresos=Sum('precio_total')
        )
        
        # Actualizar métricas básicas
        self.unidades_vendidas = ventas_periodo['total_unidades'] or 0
        self.ingresos_totales = ventas_periodo['total_ingresos'] or Decimal('0.00')
        
        if self.unidades_vendidas > 0:
            self.precio_promedio = self.ingresos_totales / self.unidades_vendidas
        else:
            self.precio_promedio = Decimal('0.00')
        
        # Calcular variación respecto al periodo anterior
        duracion_periodo = (self.fecha_fin - self.fecha_inicio).days + 1
        fecha_inicio_anterior = self.fecha_inicio - timezone.timedelta(days=duracion_periodo)
        fecha_fin_anterior = self.fecha_inicio - timezone.timedelta(days=1)
        
        ventas_periodo_anterior = VentaDetalle.objects.filter(
            producto=self.producto,
            venta__estado='completada',
            venta__fecha_creacion__date__gte=fecha_inicio_anterior,
            venta__fecha_creacion__date__lte=fecha_fin_anterior
        ).aggregate(
            total_unidades=Sum('cantidad')
        )
        
        unidades_anterior = ventas_periodo_anterior['total_unidades'] or 0
        
        # Calcular variación porcentual
        if unidades_anterior > 0:
            self.variacion_periodo_anterior = ((self.unidades_vendidas - unidades_anterior) / unidades_anterior) * 100
            
            # Determinar tendencia
            if self.variacion_periodo_anterior > 5:
                self.tendencia = 'crecimiento'
            elif self.variacion_periodo_anterior < -5:
                self.tendencia = 'decrecimiento'
            else:
                self.tendencia = 'estable'
        else:
            if self.unidades_vendidas > 0:
                self.tendencia = 'crecimiento'
                self.variacion_periodo_anterior = 100  # Aumento del 100% (de 0 a algo)
            else:
                self.tendencia = 'estable'
                self.variacion_periodo_anterior = 0
        
        self.save()
        return self