from django.test import TestCase
from app_inventario.models import Producto
from decimal import Decimal

class ProductoModelTest(TestCase):
    def setUp(self):
        # Crear un producto de prueba
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto de prueba",
            precio=Decimal('100.00'),
            cantidad_stock=10,
            stock_minimo=5
        )

    def test_producto_str_method(self):
        """Verifica el método __str__ del modelo Producto"""
        self.assertEqual(str(self.producto), "Producto Test")

    def test_stock_bajo_false(self):
        """Verifica que el método stock_bajo devuelva False cuando el stock es suficiente"""
        self.assertFalse(self.producto.stock_bajo())

    def test_stock_bajo_true(self):
        """Verifica que el método stock_bajo devuelva True cuando el stock es menor al mínimo"""
        self.producto.cantidad_stock = 3
        self.producto.save()
        self.assertTrue(self.producto.stock_bajo())

    def test_actualizar_stock(self):
        """Verifica que el stock del producto se actualice correctamente"""
        self.producto.cantidad_stock -= 2
        self.producto.save()
        self.assertEqual(self.producto.cantidad_stock, 8)

    def test_precio_producto(self):
        """Verifica que el precio del producto sea correcto"""
        self.assertEqual(self.producto.precio, Decimal('100.00'))