from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        if isinstance(value, (int, float, Decimal)):
            return float(value) * float(arg)
        return 0
    except (ValueError, TypeError):
        return 0

@register.filter(name='percentage')
def percentage(value):
    try:
        if isinstance(value, (int, float, Decimal)):
            # Multiplicar por 100 para convertir de decimal a porcentaje
            # El valor en la base de datos está entre 0 y 1
            return min(float(value) * 100, 100)
        return 0
    except (ValueError, TypeError):
        return 0

@register.filter(name='badge_class')
def badge_class(value):
    try:
        value = float(value)
        if value >= 75:
            return 'bg-success'
        elif value >= 50:
            return 'bg-info'
        elif value >= 25:
            return 'bg-warning'
        else:
            return 'bg-danger'
    except (ValueError, TypeError):
        return 'bg-danger'

@register.filter(name='stock_status')
def stock_status(current_stock, min_stock):
    try:
        if current_stock >= min_stock * 2:
            return 'success'
        elif current_stock >= min_stock:
            return 'warning'
        return 'danger'
    except (ValueError, TypeError):
        return 'danger'