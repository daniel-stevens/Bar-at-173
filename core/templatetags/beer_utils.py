from django import template
register = template.Library()

@register.filter
def beers(n):
    """
    {{ 5|beers }}  →  🍺🍺🍺🍺🍺
    """
    try:
        return "🍺" * int(n)
    except (TypeError, ValueError):
        return ""
