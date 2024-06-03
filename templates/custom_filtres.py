from django import template
register = template.Library()

@register.filter(name='starts_with_prefix')
def starts_with_prefix(value, prefix):
    return value.startswith(prefix)