from django.test import TestCase, Client
from django.urls import reverse
from app_inventario.models import Producto
from django.contrib.auth.models import User

class ProductoViewsTest(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.client = Client()
        self.client.login(username='admin', password='admin123')

        # Create a test product
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            descripcion="Descripción del producto",
            precio=100.00,
            cantidad_stock=2,
            stock_minimo=3
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('productos_bajo_stock', response.context)
        self.assertIn('num_notificaciones', response.context)

    def test_listar_productos_view(self):
        response = self.client.get(reverse('listar_productos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventarios/listar_productos.html')
        self.assertIn('productos', response.context)

    def test_registrar_producto_view_get(self):
        response = self.client.get(reverse('registrar_producto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventarios/registrar_producto.html')
        self.assertIn('form', response.context)

    def test_registrar_producto_view_post(self):
        response = self.client.post(reverse('registrar_producto'), {
            'nombre': 'Nuevo Producto',
            'descripcion': 'Descripción',
            'precio': 50.00,
            'cantidad_stock': 10,
            'stock_minimo': 5
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Producto.objects.filter(nombre='Nuevo Producto').exists())

    def test_modificar_producto_view_get(self):
        response = self.client.get(reverse('modificar_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventarios/modificar_producto.html')
        self.assertIn('form', response.context)

    def test_modificar_producto_view_post(self):
        response = self.client.post(reverse('modificar_producto', args=[self.producto.id]), {
            'nombre': 'Producto Modificado',
            'descripcion': self.producto.descripcion,
            'precio': self.producto.precio,
            'cantidad_stock': self.producto.cantidad_stock,
            'stock_minimo': self.producto.stock_minimo
        })
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Producto Modificado')

    def test_eliminar_producto_view_get(self):
        response = self.client.get(reverse('eliminar_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventarios/eliminar_producto.html')
        self.assertIn('producto', response.context)

    def test_eliminar_producto_view_post(self):
        frase_desafio = f'Eliminar "{self.producto.nombre}"'
        response = self.client.post(reverse('eliminar_producto', args=[self.producto.id]), {
            'frase_confirmacion': frase_desafio
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Producto.objects.filter(id=self.producto.id).exists())