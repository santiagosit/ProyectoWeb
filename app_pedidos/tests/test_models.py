from django.test import TestCase
from app_pedidos.models import Proveedor, Pedido, PedidoDetalle
from app_inventario.models import Producto
from django.test import TestCase, Client
from django.urls import reverse
from app_reportes.models import EstadisticaVenta, Venta
from django.utils.timezone import now
from decimal import Decimal

class ProveedorModelTest(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Test",
            telefono="123456789",
            email="proveedor@test.com",
            direccion="Dirección de prueba"
        )

    def test_str_method(self):
        self.assertEqual(str(self.proveedor), "Proveedor Test")


class PedidoModelTest(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Test",
            telefono="123456789",
            email="proveedor@test.com",
            direccion="Dirección de prueba"
        )
        self.pedido = Pedido.objects.create(proveedor=self.proveedor)

    def test_str_method(self):
        self.assertEqual(str(self.pedido), f"Pedido #{self.pedido.id} - {self.proveedor.nombre}")

    def test_total_property(self):
        producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción",
            precio=100.00,
            cantidad_stock=10,
            stock_minimo=5
        )
        PedidoDetalle.objects.create(
            pedido=self.pedido,
            producto=producto,
            cantidad=2,
            costo_unitario=50.00
        )
        self.assertEqual(self.pedido.total, 100.00)


class PedidoDetalleModelTest(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Test",
            telefono="123456789",
            email="proveedor@test.com",
            direccion="Dirección de prueba"
        )
        self.pedido = Pedido.objects.create(proveedor=self.proveedor)
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción",
            precio=100.00,
            cantidad_stock=10,
            stock_minimo=5
        )
        self.detalle = PedidoDetalle.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            cantidad=2,
            costo_unitario=50.00
        )

    def test_str_method(self):
        self.assertEqual(str(self.detalle), "Producto Test - 2 unidades")

    def test_subtotal_property(self):
        self.assertEqual(self.detalle.subtotal, 100.00)

    def test_actualizar_stock(self):
        self.detalle.actualizar_stock()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad_stock, 12)
        class EstadisticaVentaModelTest(TestCase):
            def setUp(self):
                self.producto = Producto.objects.create(
                    nombre="Producto Test",
                    descripcion="Descripción",
                    precio=100.00,
                    cantidad_stock=10,
                    stock_minimo=5
                )
                self.estadistica = EstadisticaVenta.objects.create(
                    producto=self.producto,
                    fecha=now().date(),
                    cantidad_vendida=5,
                    ingreso_total=Decimal('500.00'),
                    rotacion_inventario=Decimal('2.50'),
                    dias_sin_venta=0
                )

            def test_str_method(self):
                self.assertEqual(
                    str(self.estadistica),
                    f'Estadísticas de {self.producto.nombre} - {self.estadistica.fecha}'
                )

            def test_unique_together_constraint(self):
                with self.assertRaises(Exception):
                    EstadisticaVenta.objects.create(
                        producto=self.producto,
                        fecha=self.estadistica.fecha
                    )


        class VentaModelTest(TestCase):
            def setUp(self):
                self.producto = Producto.objects.create(
                    nombre="Producto Test",
                    descripcion="Descripción",
                    precio=100.00,
                    cantidad_stock=10,
                    stock_minimo=5
                )
                self.venta = Venta.objects.create(
                    producto=self.producto,
                    cantidad=2,
                    total=Decimal('200.00'),
                    fecha=now().date(),
                    hora=now().time(),
                    observaciones="Venta de prueba"
                )

            def test_str_method(self):
                self.assertEqual(
                    str(self.venta),
                    f'{self.producto.nombre} - {self.venta.cantidad}'
                )


        class EstadisticasVentasViewTest(TestCase):
            def setUp(self):
                self.client = Client()
                self.producto = Producto.objects.create(
                    nombre="Producto Test",
                    descripcion="Descripción",
                    precio=100.00,
                    cantidad_stock=10,
                    stock_minimo=5
                )
                self.url = reverse('reporte_inventario')

            def test_reporte_inventario_view(self):
                response = self.client.get(self.url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'reportes/estadisticas_ventas.html')

            def test_context_data(self):
                EstadisticaVenta.objects.create(
                    producto=self.producto,
                    fecha=now().date(),
                    cantidad_vendida=5,
                    ingreso_total=Decimal('500.00'),
                    rotacion_inventario=Decimal('2.50'),
                    dias_sin_venta=0
                )
                response = self.client.get(self.url)
                self.assertIn('estadisticas', response.context)
                self.assertEqual(len(response.context['estadisticas']), 1)