from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def percentage(value):
    """Convierte un valor decimal a porcentaje para barras de progreso."""
    try:
        # Asegurarse de que el valor sea un número
        value = float(value)
        
        # Para rotación de inventario, normalizar a un máximo de 100%
        if value > 1:
            return 100
        return max(0, min(100, value * 100))
    except (ValueError, TypeError):
        return 0

@register.filter
def badge_class(value):
    """Determina la clase de color para badges basado en el valor."""
    try:
        value = float(value)
        if value >= 0.75:
            return 'bg-success'
        elif value >= 0.5:
            return 'bg-info'
        elif value >= 0.25:
            return 'bg-warning'
        else:
            return 'bg-danger'
    except (ValueError, TypeError):
        return 'bg-danger'