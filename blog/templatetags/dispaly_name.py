from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # register是固定的变量名，不能改变


@register.simple_tag()          # 可以创建多个参数
def connect_name(name):
    return name + "tag function"

# print(connect_name("ddd   "))


@register.filter()      # 最多两个参数
def connect_name(name):
    return name + "tag function"