from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_usuarios.models import Profile, PIN
from django.utils.timezone import now

class UsuariosViewsTest(TestCase):
    def setUp(self):
        # Crear un usuario administrador
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_superuser=True)
        self.admin_profile = Profile.objects.create(user=self.admin_user, rol='Administrador')

        # Crear un usuario empleado
        self.employee_user = User.objects.create_user(username='employee', password='employeepassword', email='employee@example.com')
        self.employee_profile = Profile.objects.create(user=self.employee_user, rol='Empleado')

        # Cliente para realizar solicitudes
        self.client = Client()

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')

    def test_logout_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirección al login
        self.assertRedirects(response, reverse('login'))

    def test_home_view_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_employee_redirect(self):
        self.client.login(username='employee', password='employeepassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirección al dashboard de empleado
        self.assertRedirects(response, reverse('empleado_dashboard') + '?next=/home/')

    def test_empleado_dashboard_view(self):
        self.client.login(username='employee', password='employeepassword')
        response = self.client.get(reverse('empleado_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/empleado_dashboard.html')

    def test_crear_administrador_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('crear_administrador'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/Administrador/crear_administrador.html')

    def test_recuperar_password_view(self):
        response = self.client.get(reverse('recuperar_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/recuperar.html')

    def test_verificar_pin_view_correcto(self):
        # Crear un PIN válido
        pin = PIN.objects.create(user=self.employee_user, pin='123456', created_at=now())
        response = self.client.post(reverse('verificar_pin'), {
            'email': self.employee_user.email,
            'pin': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/verificar_pin.html')

    def test_verificar_pin_view_incorrecto(self):
        response = self.client.post(reverse('verificar_pin'), {
            'email': self.employee_user.email,
            'pin': 'wrongpin'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/verificar_pin.html')
        self.assertContains(response, 'PIN o correo no válido')  # Asegúrate de que este mensaje esté en la vista
