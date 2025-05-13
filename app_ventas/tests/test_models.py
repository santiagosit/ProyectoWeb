from django.test import TestCase
from app_inventario.models import Producto
from app_usuarios.models import Profile
from app_ventas.models import Venta, VentaDetalle
from decimal import Decimal
from django.contrib.auth.models import User

class VentaModelTest(TestCase):
    def setUp(self):
        # Crear un usuario y perfil para autenticación
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.empleado = Profile.objects.create(user=self.user, rol="Empleado")
        
        # Crear datos de prueba
        self.producto = Producto.objects.create(nombre="Producto Test", cantidad_stock=10, precio=Decimal('100.00'))
        self.venta = Venta.objects.create(empleado=self.empleado, total=Decimal('0.00'))

    def test_actualizar_total(self):
        detalle = VentaDetalle.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal('100.00'),
            precio_total=Decimal('200.00')
        )
        self.venta.actualizar_total()
        self.assertEqual(self.venta.total, Decimal('200.00'))

    def test_completar_venta(self):
        self.venta.completar_venta()
        self.assertEqual(self.venta.estado, 'completada')

    def test_str_method(self):
        self.assertEqual(str(self.venta), f'Venta #{self.venta.id} - pendiente')


class VentaDetalleModelTest(TestCase):
    def setUp(self):
        # Crear un usuario y perfil para autenticación
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.empleado = Profile.objects.create(user=self.user, rol="Empleado")
        
        # Crear datos de prueba
        self.producto = Producto.objects.create(nombre="Producto Test", cantidad_stock=10, precio=Decimal('100.00'))
        self.venta = Venta.objects.create(empleado=self.empleado, total=Decimal('0.00'))

    def test_save_reduces_stock(self):
        detalle = VentaDetalle.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal('100.00'),
            precio_total=Decimal('200.00')
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad_stock, 8)

    def test_delete_restores_stock(self):
        detalle = VentaDetalle.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal('100.00'),
            precio_total=Decimal('200.00')
        )
        detalle.delete()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad_stock, 10)