import datetime
from django.db import models
from django.utils import timezone, text
from django.template.response import TemplateResponse

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
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from taggit.models import TaggedItemBase


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey('projects.ProjectPage',
                                 related_name='tagged_items')


class SkillTag(TaggedItemBase):
    content_object = ParentalKey('projects.ProjectPage',
                                 related_name='skill_items')


class ProjectIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['projects.ProjectPage']

    def create_test(title, intro, parent=None):
        if (parent is None):
            parent = Page.get_first_root_node()
        project_idx = ProjectIndexPage(title=title, intro=intro,
                                       slug=text.slugify(title))
        parent.add_child(instance=project_idx)
        return project_idx

    @route(r'^$')
    def base(self, request):
        """
        Index view with all projects
        """
        context = super(ProjectIndexPage, self).get_context(request)
        projects = ProjectPage.objects.child_of(self) \
            .order_by('-project_date').live()
        context['projects'] = projects
        context['total_items'] = len(projects)

        return TemplateResponse(
          request,
          self.get_template(request),
          context
        )

    @route(r'^s/(.+)/$', name='skilltag')
    def tagged_projects(self, request, tag):
        """
        View function for filtered projects view
        """
        context = super(ProjectIndexPage, self).get_context(request)
        projects = ProjectPage.objects.child_of(self) \
            .order_by('-project_date').filter(
                skill_tags__name__in=[tag]
            ).distinct().live()
        context['projects'] = projects
        context['total_items'] = ProjectPage.objects.child_of(self) \
            .live().count()

        return TemplateResponse(
          request,
          self.get_template(request),
          context
        )

    @route(r'^t/(.+)/$', name='filter')
    def filtered_projects(self, request, tag):
        """
        View function for filtered projects view
        """
        context = super(ProjectIndexPage, self).get_context(request)
        projects = ProjectPage.objects.child_of(self) \
            .order_by('-project_date').filter(
                tags__name__in=[tag]
            ).distinct().live()
        context['projects'] = projects
        context['total_items'] = ProjectPage.objects.child_of(self) \
            .live().count()
        context['current_tag'] = tag

        return TemplateResponse(
          request,
          self.get_template(request),
          context
        )


class ProjectPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    project_date = models.DateField("Projektdatum")
    lead = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)
    tags.rel.related_name = '+'
    skill_tags = ClusterTaggableManager(through=SkillTag, blank=True)
    skill_tags.rel.related_name = '+'
    project_url = models.CharField(max_length=250, default='')
    column1 = RichTextField('Spalte 1 (Briefing)', blank=True)
    column2 = RichTextField('Spalte 2 (Lösungsansatz)', blank=True)

    parent_page_types = [
        'projects.ProjectIndexPage',
    ]

    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('lead'),
        index.SearchField('column1'),
        index.SearchField('column2'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('project_date'),
        ImageChooserPanel('main_image'),
        FieldPanel('lead'),
        FieldPanel('project_url'),
        FieldPanel('skill_tags'),
        MultiFieldPanel([
            FieldPanel('column1', classname='full'),
            FieldPanel('column2', classname='full'),
        ], 'Inhalt')
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
