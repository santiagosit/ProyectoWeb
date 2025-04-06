from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='percentage')
def percentage(value):
    try:
        if isinstance(value, (int, float, Decimal)):
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

@register.filter(name='color_class')
def color_class(value):
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