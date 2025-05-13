from django.test import TestCase
from django.contrib.auth.models import User
from app_usuarios.models import Profile, PIN
from django.utils.timezone import now, timedelta

class ProfileModelTest(TestCase):
    def setUp(self):
        # Crear un usuario
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.profile = Profile.objects.create(
            user=self.user,
            nombre_completo="Test User",
            telefono="123456789",
            direccion="Test Address",
            fecha_contratacion="2023-01-01",
            rol="Empleado"
        )

    def test_profile_creation(self):
        """Verifica que el perfil se haya creado correctamente"""
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.nombre_completo, "Test User")
        self.assertEqual(self.profile.rol, "Empleado")

    def test_profile_str_method(self):
        """Verifica el método __str__ del modelo Profile"""
        self.assertEqual(str(self.profile), "testuser (Empleado)")

    def test_superuser_str_method(self):
        """Verifica el método __str__ para un superusuario"""
        self.user.is_superuser = True
        self.user.save()
        self.assertEqual(str(self.profile), "testuser (Superusuario)")

    def test_unique_user_constraint(self):
        """Verifica que no se puedan crear dos perfiles para el mismo usuario"""
        with self.assertRaises(Exception):
            Profile.objects.create(
                user=self.user,
                nombre_completo="Duplicate User",
                telefono="987654321",
                direccion="Duplicate Address",
                fecha_contratacion="2023-01-01",
                rol="Administrador"
            )


class PINModelTest(TestCase):
    def setUp(self):
        # Crear un usuario
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.pin = PIN.objects.create(user=self.user, pin="123456", created_at=now())

    def test_pin_creation(self):
        """Verifica que el PIN se haya creado correctamente"""
        self.assertEqual(self.pin.user.username, "testuser")
        self.assertEqual(self.pin.pin, "123456")

    def test_pin_str_method(self):
        """Verifica el método __str__ del modelo PIN"""
        self.assertEqual(str(self.pin), "testuser - 123456")

    def test_pin_is_valid(self):
        """Verifica que el método is_valid siempre devuelva True"""
        self.assertTrue(self.pin.is_valid())

    def test_pin_is_expired(self):
        """Verifica que el método is_expired funcione correctamente"""
        self.pin.created_at = now() - timedelta(minutes=11)
        self.assertTrue(self.pin.is_expired())

        self.pin.created_at = now() - timedelta(minutes=9)
        self.assertFalse(self.pin.is_expired())