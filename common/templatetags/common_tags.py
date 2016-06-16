from django.template.defaulttags import register

from common.models import *

register = template.Library()


@register.filter
def svalue(structvalue, key):
    return structvalue[key]


@register.inclusion_tag('tags/social_links.html', takes_context=True)
def social_links(context):
    return {
        'social_links': SocialLink.objects.all(),
        'request': context['request'],
    }
