from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel

from projects.models import ProjectPage


class HomePage(Page):
    heading = models.CharField(max_length=100, default='')
    lead = models.CharField(max_length=150, default='')

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('lead')
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        # Add extra variables and return the updated context
        context['projects'] = ProjectPage.objects.child_of(self).live()
        return context
