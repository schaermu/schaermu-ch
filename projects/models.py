from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
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

    def get_context(self, request):
        context = super(ProjectIndexPage, self).get_context(request)

        # Add extra variables and return the updated context
        context['projects'] = ProjectPage.objects.child_of(self).live()
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
    name = models.CharField(max_length=100)
    lead = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)

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
        FieldPanel('name'),
        ImageChooserPanel('main_image'),
        FieldPanel('lead'),
        FieldPanel('body', classname="full")
    ]

    def get_latest(limit=3):
        return ProjectPage.objects.live().order_by('-project_date').all()[:limit]
