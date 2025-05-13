from django.test import TestCase
from app_eventos.models import Cliente, Evento
from django.utils import timezone
from datetime import timedelta

class ClienteModelTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Test Cliente",
            telefono="123456789",
            email="test@cliente.com",
            direccion="Test Address"
        )

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nombre, "Test Cliente")
        self.assertEqual(self.cliente.telefono, "123456789")
        self.assertEqual(self.cliente.email, "test@cliente.com")
        self.assertEqual(self.cliente.direccion, "Test Address")
        self.assertIsNotNone(self.cliente.fecha_registro)

    def test_cliente_str_representation(self):
        self.assertEqual(str(self.cliente), "Test Cliente - 123456789")


class EventoModelTestCase(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Test Cliente",
            telefono="123456789",
            email="test@cliente.com"
        )
        self.evento = Evento.objects.create(
            cliente=self.cliente,
            descripcion="Test Evento",
            fecha_evento=timezone.now() + timedelta(days=1),
            estado="Pendiente"
        )

    def test_evento_creation(self):
        self.assertEqual(self.evento.cliente, self.cliente)
        self.assertEqual(self.evento.descripcion, "Test Evento")
        self.assertEqual(self.evento.estado, "Pendiente")
        self.assertIsNotNone(self.evento.fecha_evento)

    def test_evento_str_representation(self):
        self.assertEqual(
            str(self.evento),
            f"Evento de {self.cliente.nombre} - {self.evento.fecha_evento}"
        )