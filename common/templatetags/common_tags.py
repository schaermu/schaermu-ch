from django.template.defaulttags import register

from projects.models import ProjectPageTag
from common.models import *

register = template.Library()


@register.filter
def svalue(structvalue, key):
    return structvalue[key]


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


@register.inclusion_tag('tags/social_links.html', takes_context=True)
def social_links(context):
    return {
        'social_links': SocialLink.objects.all(),
        'request': context['request'],
    }


@register.inclusion_tag('tags/menu_items.html', takes_context=True)
def menu_items(context, parent, calling_page=None):
    menuitems = parent.get_children().live()

    for menuitem in menuitems:
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)

    return {
        'parent': parent,
        'children': menuitems,
        'request': context['request'],
    }


@register.inclusion_tag('tags/project_filter.html', takes_context=True)
def project_filter(context, page, total_items, current_tag):
    return {
        'page': page,
        'total_items': total_items,
        'current_tag': current_tag,
        'request': context['request']
    }
