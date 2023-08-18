from django import template

register = template.Library()

def to_and(value):
    return value.replace("\n","</br>")

register.filter("to_and", to_and)