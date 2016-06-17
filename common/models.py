from django.db import models
from django import template

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class SocialLink(models.Model):
    url = models.URLField(null=True, blank=True)
    icon = models.CharField(max_length=20)

    panels = [
        FieldPanel('url'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.url
