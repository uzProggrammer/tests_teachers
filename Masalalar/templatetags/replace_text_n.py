from django import template

register = template.Library()


@register.filter
def replace_text(value):
    return value.replace("\\n", "<br>")