# products/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def get_item(value, key):
    """Allow list/dict indexing in templates"""
    try:
        return value[key]
    except (IndexError, KeyError, TypeError):
        return ''
