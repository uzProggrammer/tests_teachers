from django import template

register = template.Library()


@register.filter
def get_c(value):
    return value.replace("\\n", "<br>")

@register.filter
def get_1_2(value):
    return value.masalalar.count()+value.topshiriqlar.count()