from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

from app_finanzas.models import Ingreso, Egreso


class FinanzasViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='1234',
            is_superuser=True,
            is_staff=True
        )
        self.client.login(username='admin', password='1234')

        self.ingreso = Ingreso.objects.create(
            monto=Decimal('100.00'),
            descripcion='Test ingreso',
            tipo='personalizado',
            fecha=timezone.now()
        )

        self.egreso = Egreso.objects.create(
            monto=Decimal('50.00'),
            descripcion='Test egreso',
            tipo='personalizado',
            fecha=timezone.now()
        )

    def test_listar_ingresos_status_and_template(self):
        response = self.client.get(reverse('listar_ingresos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finanzas/listar_ingresos.html')

    def test_detalle_ingreso_status_and_template(self):
        response = self.client.get(reverse('detalle_ingreso', args=[self.ingreso.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finanzas/detalle_ingreso.html')

    def test_eliminar_ingreso_post(self):
        response = self.client.post(reverse('eliminar_ingreso', args=[self.ingreso.id]))
        self.assertRedirects(response, reverse('listar_ingresos'))
        self.assertFalse(Ingreso.objects.filter(id=self.ingreso.id).exists())

    def test_crear_ingreso_personalizado_valido(self):
        response = self.client.post(reverse('crear_ingreso_personalizado'), {
            'monto': '200.00',
            'descripcion': 'Nuevo ingreso',
        })
        self.assertRedirects(response, reverse('listar_ingresos'))
        self.assertTrue(Ingreso.objects.filter(descripcion='Nuevo ingreso').exists())

    def test_listar_egresos_status_and_template(self):
        response = self.client.get(reverse('listar_egresos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finanzas/listar_egresos.html')

    def test_detalle_egreso_status_and_template(self):
        response = self.client.get(reverse('detalle_egreso', args=[self.egreso.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finanzas/detalle_egreso.html')

    def test_eliminar_egreso_post(self):
        response = self.client.post(reverse('eliminar_egreso', args=[self.egreso.id]))
        self.assertRedirects(response, reverse('listar_egresos'))
        self.assertFalse(Egreso.objects.filter(id=self.egreso.id).exists())

