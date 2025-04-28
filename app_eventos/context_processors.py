from .views import get_eventos_proximos

def notificaciones_eventos(request):
    """
    Contexto para notificaciones de eventos próximos (3 días)
    """
    eventos_proximos = get_eventos_proximos()
    return {
        'eventos_proximos_notificacion': eventos_proximos,
        'num_notificaciones_eventos': eventos_proximos.count(),
    }
