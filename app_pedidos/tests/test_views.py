from django.test import TestCase, Client
from django.urls import reverse
from app_pedidos.models import Proveedor, Pedido, PedidoDetalle
from app_inventario.models import Producto
from django.contrib.auth.models import User

class PedidoViewsTest(TestCase):
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

    def test_listar_pedidos_view(self):
        response = self.client.get(reverse('listar_pedidos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pedidos/listar_pedidos.html')
        self.assertIn('pedidos', response.context)

    def test_registrar_pedido_view_get(self):
        response = self.client.get(reverse('registrar_pedido'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pedidos/registrar_pedido.html')
        self.assertIn('pedido_form', response.context)


    def test_actualizar_estado_pedido_view_get(self):
        response = self.client.get(reverse('actualizar_estado_pedido', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pedidos/actualizar_estado_pedido.html')
        self.assertIn('pedido', response.context)

    def test_actualizar_estado_pedido_view_post(self):
        response = self.client.post(reverse('actualizar_estado_pedido', args=[self.pedido.id]), {
            'estado': 'recibido'
        })
        self.assertEqual(response.status_code, 302)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.estado, 'recibido')

    def test_detalles_pedido_view(self):
        response = self.client.get(reverse('detalles_pedido', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pedidos/detalles_pedido.html')
        self.assertIn('pedido', response.context)
        self.assertIn('detalles', response.context)
