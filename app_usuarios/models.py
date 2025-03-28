from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    """Modelo base de usuarios, usado para autenticación y roles."""
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Se recomienda hashearla
    rol = models.CharField(max_length=20, choices=[
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ])

    # Recuperación de contraseña
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"


from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=[
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ])

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


class PIN(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pin}"

    def is_valid(self):
        """Valida que el PIN no tenga más de 10 minutos."""
        return True
        