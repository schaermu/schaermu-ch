from django.template.defaulttags import register


@register.filter
def svalue(structvalue, key):
    return structvalue[key]
