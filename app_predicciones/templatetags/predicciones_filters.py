from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    """
    Obtiene un elemento de una secuencia (lista, tupla) por su índice.
    Ejemplo de uso: {{ meses|index:mes_num }}
    """
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return None
