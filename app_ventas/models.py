from django.db import models
from app_inventario.models import Producto
from app_usuarios.models import Usuario  # Relación con el usuario empleado

class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Campo para el total de la venta
    empleado = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'rol': 'Empleado'})

    def __str__(self):
        return f'Venta {self.id}'

    def calcular_total(self):
        self.total = sum(detalle.subtotal() for detalle in self.detalles.all())
        self.save()


class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.venta.calcular_total()  # Recalcular el total de la venta cada vez que se guarda un detalle.
