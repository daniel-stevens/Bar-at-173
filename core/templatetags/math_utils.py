from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply two numbers in templates: {{ x|mul:y }}"""
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0

@register.filter
def div(value, arg):
    """Divide two numbers in templates: {{ x|div:y }}"""
    try:
        return float(value) / float(arg)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0
