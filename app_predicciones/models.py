from django.db import models
from app_inventario.models import Producto
from django.utils import timezone
from decimal import Decimal

class PrediccionVenta(models.Model):
    ESTADO_PREDICCION = [
        ('alta', 'Alta Demanda'),
        ('media', 'Demanda Media'),
        ('baja', 'Baja Demanda'),
        ('riesgo', 'Riesgo de Sobre-stock')
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='predicciones')
    fecha_prediccion = models.DateTimeField(default=timezone.now)
    fecha_inicio_analisis = models.DateField()
    fecha_fin_analisis = models.DateField()
    ventas_promedio = models.DecimalField(max_digits=10, decimal_places=2)
    tendencia = models.CharField(max_length=20, choices=ESTADO_PREDICCION)
    confianza_prediccion = models.DecimalField(max_digits=5, decimal_places=2)
    cantidad_sugerida = models.PositiveIntegerField()
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_prediccion']

    def __str__(self):
        return f'Predicción para {self.producto.nombre} - {self.tendencia}'

class EstadisticaVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='estadisticas')
    fecha = models.DateField()
    cantidad_vendida = models.PositiveIntegerField(default=0)
    ingreso_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    rotacion_inventario = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    dias_sin_venta = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['producto', 'fecha']
        ordering = ['-fecha']

    def __str__(self):
        return f'Estadísticas de {self.producto.nombre} - {self.fecha}'