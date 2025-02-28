from django.db import models
from app_inventario.models import Producto

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(default='default@example.com')  # Asegúrate que esta línea esté presente


    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pedido', 'Pedido'),
        ('en camino', 'En camino'),
        ('recibido', 'Recibido'),
    ], default='pedido')

    def detalles(self):
        return self.pedidodetalle_set.all()

    def __str__(self):
        return f'Pedido {self.id} - {self.proveedor.nombre}'

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Añadir costo unitario

    def subtotal(self):
        return self.cantidad * self.costo_unitario  # Calcular el subtotal por producto

    def actualizar_stock(self):
        self.producto.cantidad_stock += self.cantidad
        self.producto.save()




