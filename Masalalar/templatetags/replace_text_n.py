from django import template
from sinflar.models import Sinf

register = template.Library()


@register.filter
def replace_text(value):
    return value.replace("\\n", "<br>")


@register.filter
def get_class(value):
    try:
        sinf = Sinf.objects.get(nom=value.sinf)
        return sinf.url
    except:
        return False