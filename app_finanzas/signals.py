from django.db.models.signals import post_save
from django.dispatch import receiver
from app_ventas.models import Venta
from app_pedidos.models import Pedido
from .models import Ingreso, Egreso
from django.db import transaction

@receiver(post_save, sender=Venta)
def crear_ingreso_por_venta(sender, instance, created, **kwargs):
    if created:
        Ingreso.objects.create(
            venta=instance,
            monto=instance.total,
            descripcion=f'Ingreso por Venta ID {instance.id}'
        )

@receiver(post_save, sender=Pedido)
def crear_egreso_por_pedido(sender, instance, created, **kwargs):
    # Solo crear Egreso cuando el pedido cambia a 'recibido'
    if not created:
        if instance.estado == 'recibido' and not hasattr(instance, 'egreso'):
            # Calcula el monto total del pedido
            total_pedido = 0
            for detalle in instance.detalles():
                # Asumiendo que 'precio' en Producto es el costo para el egreso
                total_pedido += detalle.cantidad * detalle.producto.precio

            Egreso.objects.create(
                pedido=instance,
                monto=total_pedido,
                descripcion=f'Egreso por Pedido ID {instance.id}'
            )
