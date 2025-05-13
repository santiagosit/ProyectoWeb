from django.test import TestCase
from app_inventario.models import Producto
from app_reportes.models import EstadisticaVenta, Venta
from decimal import Decimal
from django.utils.timezone import now

class EstadisticaVentaModelTest(TestCase):
    def setUp(self):
        # Crear un producto de prueba
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            cantidad_stock=10,
            stock_minimo=5,
            precio=Decimal('100.00')
        )

        # Crear una estadística de venta
        self.estadistica = EstadisticaVenta.objects.create(
            producto=self.producto,
            fecha=now().date(),
            cantidad_vendida=5,
            ingreso_total=Decimal('500.00'),
            rotacion_inventario=1.5,
            dias_sin_venta=2
        )

    def test_estadistica_str_method(self):
        """Verifica el método __str__ del modelo EstadisticaVenta"""
        self.assertEqual(
            str(self.estadistica),
            f'Estadísticas de {self.producto.nombre} - {self.estadistica.fecha}'
        )

    def test_unique_constraint(self):
        """Verifica que no se puedan crear dos estadísticas para el mismo producto y fecha"""
        with self.assertRaises(Exception):
            EstadisticaVenta.objects.create(
                producto=self.producto,
                fecha=now().date(),
                cantidad_vendida=3,
                ingreso_total=Decimal('300.00'),
                rotacion_inventario=1.0,
                dias_sin_venta=1
            )


class VentaModelTest(TestCase):
    def setUp(self):
        # Crear un producto de prueba
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            cantidad_stock=10,
            stock_minimo=5,
            precio=Decimal('100.00')
        )

        # Crear una venta
        self.venta = Venta.objects.create(
            producto=self.producto,
            cantidad=2,
            total=Decimal('200.00'),
            fecha=now().date(),
            hora=now().time(),
            observaciones="Venta de prueba"
        )

    def test_venta_str_method(self):
        """Verifica el método __str__ del modelo Venta"""
        self.assertEqual(
            str(self.venta),
            f'{self.producto.nombre} - {self.venta.cantidad}'
        )

    def test_total_calculation(self):
        """Verifica que el total de la venta sea correcto"""
        self.assertEqual(self.venta.total, Decimal('200.00'))


    def test_stock_restoration_on_delete(self):
        """Verifica que el stock del producto se restaure al eliminar una venta"""
        self.venta.delete()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad_stock, 10)