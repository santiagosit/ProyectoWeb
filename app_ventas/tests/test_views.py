from django.test import TestCase, Client
from django.urls import reverse
from app_inventario.models import Producto
from app_usuarios.models import Profile
from app_ventas.models import Venta
from decimal import Decimal
from django.contrib.auth.models import User

class VentaViewsTest(TestCase):
    def setUp(self):
        # Crear un usuario y perfil para autenticación
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, rol="Empleado")
        
        # Autenticar al cliente
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Crear datos de prueba
        self.producto = Producto.objects.create(nombre="Producto Test", cantidad_stock=10, precio=Decimal('100.00'))
        self.venta = Venta.objects.create(empleado=self.profile, total=Decimal('0.00'))

    def test_registrar_venta_view(self):
        response = self.client.get(reverse('registrar_venta'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ventas/registrar_venta.html')

    def test_detalle_venta_view(self):
        response = self.client.get(reverse('detalle_venta', args=[self.venta.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ventas/detalle_venta_empleado.html')

