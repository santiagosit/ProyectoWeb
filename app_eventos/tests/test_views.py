from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_eventos.models import Evento, Cliente
from django.utils import timezone
from datetime import timedelta

class EventosViewsTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_superuser=True)
        self.employee_user = User.objects.create_user(username='employee', password='employeepass', is_staff=True)
        
        # Create test client
        self.client = Client()

        # Create test cliente and evento
        self.cliente = Cliente.objects.create(nombre='Test Cliente', telefono='123456789', email='test@cliente.com')
        self.evento = Evento.objects.create(
            cliente=self.cliente,
            descripcion='Test Evento',
            fecha_evento=timezone.now() + timedelta(days=1),
            estado='Pendiente'
        )

    def test_listar_eventos_as_employee(self):
        self.client.login(username='employee', password='employeepass')
        response = self.client.get(reverse('listar_eventos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/listar_eventos.html')
        self.assertContains(response, 'Test Evento')

    def test_crear_evento_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('crear_evento'), {
            'nombre': 'Nuevo Cliente',
            'telefono': '987654321',
            'email': 'nuevo@cliente.com',
            'descripcion': 'Nuevo Evento',
            'fecha_evento': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Evento.objects.filter(descripcion='Nuevo Evento').exists())

    def test_eliminar_evento_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('eliminar_evento', args=[self.evento.id]), {'confirmar': 'si'})
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Evento.objects.filter(id=self.evento.id).exists())

    def test_access_denied_for_non_authenticated_users(self):
        response = self.client.get(reverse('listar_eventos'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        response = self.client.get(reverse('crear_evento'))
        self.assertEqual(response.status_code, 302)  # Redirect to login