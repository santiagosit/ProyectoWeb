from django.test import TestCase, Client
from django.urls import reverse
from app_inventario.models import Producto
from app_inventario.forms import ProductoForm

class ProductoModelTest(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            precio=100.00,
            cantidad_stock=2,
            stock_minimo=3
        )

    def test_str_method(self):
        self.assertEqual(str(self.producto), "Producto Test")

    def test_stock_bajo(self):
        self.assertTrue(self.producto.stock_bajo())
        self.producto.cantidad_stock = 5
        self.assertFalse(self.producto.stock_bajo())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            precio=100.00,
            cantidad_stock=2,
            stock_minimo=3
        )
        self.admin_login_url = reverse('empleado_dashboard')

    def test_listar_productos_view(self):
        response = self.client.get(reverse('listar_productos'))
        self.assertEqual(response.status_code, 302)  # Redirect to login for unauthenticated users
