from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
  #returns list from string separated by key
  return value.split(key)