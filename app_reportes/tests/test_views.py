from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_inventario.models import Producto
from app_reportes.models import Venta, EstadisticaVenta
from django.utils.timezone import now

class ReportesViewsTest(TestCase):
    def setUp(self):
        # Crear un usuario administrador
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_superuser=True)
        self.client = Client()
        self.client.login(username='admin', password='adminpassword')

        # Crear datos de prueba
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            cantidad_stock=10,
            stock_minimo=5,
            precio=100.00  # Agregar el campo precio
        )
        self.venta = Venta.objects.create(
            producto=self.producto,
            cantidad=2,
            total=200.00,
            fecha=now().date(),
            hora=now().time(),
            observaciones="Venta de prueba"
        )
        self.estadistica = EstadisticaVenta.objects.create(
            producto=self.producto,
            fecha=now().date(),
            cantidad_vendida=2,
            ingreso_total=200.00,
            rotacion_inventario=1.5,
            dias_sin_venta=0
        )

    def test_reporte_inventario_view(self):
        response = self.client.get(reverse('reporte_inventario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportes/reporte_inventario.html')
        self.assertIn('productos_mas_vendidos', response.context)
        self.assertIn('productos_sin_stock', response.context)
        self.assertIn('productos_agotandose', response.context)
        self.assertIn('productos_no_vendidos', response.context)

    def test_reporte_ingresos_egresos_view(self):
        response = self.client.get(reverse('reporte_ingresos_egresos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportes/reporte_ingresos_egresos.html')
        self.assertIn('total_ingresos', response.context)
        self.assertIn('total_egresos', response.context)
        self.assertIn('balance', response.context)

    def test_exportar_reporte_excel_view(self):
        response = self.client.get(reverse('exportar_reporte_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_exportar_reporte_financiero_view(self):
        response = self.client.get(reverse('exportar_reporte_financiero'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_exportar_reporte_pdf_view(self):
        response = self.client.get(reverse('exportar_reporte_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')