from django.test import TestCase, Client
from django.urls import reverse
from app_inventario.models import Producto
from app_pedidos.models import Pedido, PedidoDetalle, Proveedor
from django.contrib.auth.models import User

class PrediccionesViewsTest(TestCase):
    def setUp(self):
        # Crear un usuario administrador y loguearlo
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.client = Client()
        self.client.login(username='admin', password='admin123')

        # Crear datos de prueba
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Test",
            telefono="123456789",
            email="proveedor@test.com",
            direccion="Dirección de prueba"
        )
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción",
            precio=100.00,
            cantidad_stock=10,
            stock_minimo=5
        )
        self.pedido = Pedido.objects.create(proveedor=self.proveedor)
        self.detalle = PedidoDetalle.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            cantidad=2,
            costo_unitario=50.00
        )


    def test_oportunidad_compra_prediccion_view_with_producto(self):
        response = self.client.get(reverse('predicciones:oportunidad_compra'), {'producto': self.producto.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'predicciones/oportunidad_compra.html')
        self.assertEqual(response.context['producto_seleccionado'], self.producto)
        self.assertIn('labels', response.context)
        self.assertIn('data_historico', response.context)


    def test_dashboard_predicciones_view_with_producto(self):
        response = self.client.get(reverse('predicciones:dashboard'), {'producto': self.producto.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'predicciones/dashboard.html')
        self.assertEqual(response.context['producto_seleccionado'], self.producto)
        self.assertIn('demanda_proyectada', response.context)
        self.assertIn('fecha_sugerida', response.context)

from django.test import TestCase

class BasicTest(TestCase):
    def test_basic(self):
        self.assertEqual(1 + 1, 2)