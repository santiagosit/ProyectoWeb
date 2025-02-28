import logging
from django.shortcuts import redirect
from django.urls import reverse, resolve

logger = logging.getLogger(__name__)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de nombres de vistas exentas
        exempt_views = [
            'login',  # Nombre de la URL que has definido en urls.py para el login
            'registrar_usuario',  # Nombre de la URL para registrar
            'recuperar_password',  # Nombre de la URL para recuperar contraseña
            'verificar_pin',  # Nombre de la URL para verificar el pin
            'enviar_pin',  # Nombre de la URL para enviar el pin
        ]

        # Obtener la vista que se está resolviendo
        resolver = resolve(request.path_info)
        view_name = resolver.url_name  # Nombre de la vista actual

        logger.debug(f"Request path: {request.path}")
        logger.debug(f"Exempt views: {exempt_views}")
        logger.debug(f"Current view name: {view_name}")

        # Si el usuario no está autenticado y la vista no está exenta, redirigir al login
        if not request.user.is_authenticated and view_name not in exempt_views:
            logger.debug("Redirecting to login")
            return redirect('login')

        # Continuar con el flujo de la aplicación
        response = self.get_response(request)
        return response
