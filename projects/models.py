import datetime
from django.db import models
from django.utils import timezone, text

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                InlinePanel, StreamFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey('projects.ProjectPage',
                                 related_name='tagged_items')


class ProjectIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def create_test(title, intro, parent=None):
        if (parent is None):
            parent = Page.get_first_root_node()
        project_idx = ProjectIndexPage(title=title, intro=intro,
                                       slug=text.slugify(title))
        parent.add_child(instance=project_idx)
        return project_idx

    def get_context(self, request):
        context = super(ProjectIndexPage, self).get_context(request)

        # Add extra variables and return the updated context
        context['projects'] = ProjectPage.objects.child_of(self) \
            .order_by('-project_date').live()
        return context


class ProjectPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    project_date = models.DateField("Projektdatum")
    lead = models.CharField(max_length=250)
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname='full title', label='Titel',
                                     icon='title')),
        ('paragraph', blocks.RichTextBlock(label='Absatz')),
        ('image', ImageChooserBlock(label='Bild')),
        ('gallery', blocks.ListBlock(ImageChooserBlock(label='Bild'),
                                     label='Bildgalerie',
                                     template='blocks/gallery.html',
                                     icon='grip'))
    ])

    parent_page_types = [
        'projects.ProjectIndexPage',
    ]

    search_fields = Page.search_fields + [
        index.SearchField('lead'),
        index.SearchField('body'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('project_date'),
        ImageChooserPanel('main_image'),
        FieldPanel('lead'),
        StreamFieldPanel('body')
    ]

    def get_latest(limit=4):
        return ProjectPage.objects.live().order_by('-project_date') \
            .all()[:limit]

    def create_test(title, lead, day_offset, parent_page):
        proj_date = timezone.now() + datetime.timedelta(days=day_offset)
        project_page = ProjectPage(title=title, lead=lead,
                                   slug=text.slugify(title),
                                   project_date=proj_date)
        parent_page.add_child(instance=project_page)
        return project_page
