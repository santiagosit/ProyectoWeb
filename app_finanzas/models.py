from django.db import models
from app_ventas.models import Venta
from app_pedidos.models import Pedido

class Ingreso(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='ingreso')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Ingreso - Venta {self.venta.id} - {self.monto}'

# app_finanzas/models.py
class Egreso(models.Model):
    TIPO_CHOICES = [
        ('pedido', 'Pedido'),
        ('personalizado', 'Personalizado')
    ]
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='pedido')
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='egreso', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100, default='Pedido')  # Categoría personalizada

    def __str__(self):
        return f'Egreso - {self.tipo.capitalize()} - {self.monto}'

