from django import template

register = template.Library()

@register.filter
def get_item(d, key):
    """
    Dictionary lookup inside templates:
    {{ mydict|get_item:the_key }}
    """
    try:
        return d.get(key)
    except (AttributeError, TypeError):
        return None
