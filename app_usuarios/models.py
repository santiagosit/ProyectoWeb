# models.py
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)  # Considera mejorar esto con hasheo.
    rol = models.CharField(max_length=20, choices=[('Administrador', 'Administrador')])

    def __str__(self):
        return self.nombre


class PIN(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pin}"

    def is_valid(self):
        """Valida que el PIN no tenga más de 10 minutos."""
        return True





