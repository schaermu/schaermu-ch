from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils import timezone, text

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                InlinePanel, StreamFieldPanel)
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from projects.models import ProjectPage


class CareerItemBlock(blocks.StructBlock):
    url = blocks.URLBlock(max_length=250, default='', label='URL')
    name = blocks.CharBlock(max_length=150, default='', label='Firma')
    start_date = blocks.DateBlock(label='Datum Antritt')
    end_date = blocks.DateBlock(label='Datum Austritt')
    text = blocks.RichTextBlock(label='Beschreibung')

    class Meta:
        template = 'blocks/career_item.html'


class HomePage(Page):
    heading = models.CharField(max_length=100, default='')
    lead = models.CharField(max_length=150, default='')
    portrait_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('heading', blocks.CharBlock(classname='full title', label='Titel')),
        ('paragraph', blocks.RichTextBlock(label='Absatz')),
        ('image', ImageChooserBlock(label='Bild')),
        ('career', blocks.ListBlock(CareerItemBlock, label='Karriere',
                                    template='blocks/career.html',
                                    icon='user'))
    ])

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('lead'),
        ImageChooserPanel('portrait_image'),
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
