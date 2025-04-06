from django.db import models
from app_inventario.models import Producto
from decimal import Decimal


class EstadisticaVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='estadisticas_reporte')
    fecha = models.DateField()
    cantidad_vendida = models.PositiveIntegerField(default=0)
    ingreso_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    rotacion_inventario = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    dias_sin_venta = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['producto', 'fecha']
        ordering = ['-fecha']
        verbose_name = 'Estadística de Venta'
        verbose_name_plural = 'Estadísticas de Ventas'

    def __str__(self):
        return f'Estadísticas de {self.producto.nombre} - {self.fecha}'


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas_reportes')
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    hora = models.TimeField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad}'
