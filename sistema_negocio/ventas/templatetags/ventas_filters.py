from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Obtener un item de un diccionario por clave"""
    if dictionary is None:
        return None
    return dictionary.get(key, 0)

