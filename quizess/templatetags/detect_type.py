from django import template

register = template.Library()

@register.filter
def detect_type(element):
    return str(type(element))

@register.filter
def get_range_with_len(element):
    d = {}
    i=1
    for j in element:
        d[i] = j
        i+=1

    return d.items()

@register.filter
def add_qirq(value, page):
    value,page = int(value), int(page)
    return value+(page-1)*40

@register.filter
def get_user_result(value, user):
    res = value.results.filter(user=user)
    if res.count() != 0:
        return res.first().get_trues()
    else:
        return 0