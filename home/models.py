from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils import timezone, text

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                InlinePanel, StreamFieldPanel)
from wagtail.wagtailimages.blocks import ImageChooserBlock

from projects.models import ProjectPage


class HomePage(Page):
    heading = models.CharField(max_length=100, default='')
    lead = models.CharField(max_length=150, default='')
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('lead'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        context['latest_projects'] = ProjectPage.get_latest()
        return context

    def create_test(title, lead):
        parent_page = Page.get_first_root_node()
        home = HomePage(heading=title, title=title, lead=lead,
                        slug=text.slugify(title))
        parent_page.add_child(instance=home)
        return home
