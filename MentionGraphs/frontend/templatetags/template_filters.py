from django import template
register = template.Library()

@register.filter("hash")
def hash(h, key):
    if isinstance(h, dict):
        return h[key]
    else:
        return ''
