from django import template

register = template.Library()

@register.filter
def percentage(value):
    """Convierte un valor decimal a porcentaje (0-100)"""
    try:
        value = float(value)
        # Asegurarse que el valor esté entre 0 y 1
        if value < 0:
            return 0
        if value > 1:
            return 100
        return value * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def badge_class(value):
    """Determina la clase de color para badges basado en el valor"""
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