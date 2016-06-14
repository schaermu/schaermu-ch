import datetime
from django.test import TestCase
from django.utils import timezone, text
from .models import ProjectPage, ProjectIndexPage
from wagtail.wagtailcore.models import Page


def create_project_page(name, lead, body, day_offset, parent_page):
    proj_date = timezone.now() + datetime.timedelta(days=day_offset)
    project_page = ProjectPage(name=name, title=name, lead=lead, body=body,
                               slug=text.slugify(name), project_date=proj_date)
    parent_page.add_child(instance=project_page)
    return project_page


def create_project_index_page(title, intro):
    parent_page = Page.get_first_root_node()
    project_idx = ProjectIndexPage(title=title, intro=intro,
                                   slug=text.slugify(title))
    parent_page.add_child(instance=project_idx)
    return project_idx


# Create your tests here.
class ProjectPageTests(TestCase):
    def test_get_latest_returns_latest_projects(self):
        project_index = create_project_index_page('test index', 'test')
        create_project_page('test page 1', 'test', 'test', 2, project_index)
        create_project_page('test page 2', 'test', 'test', 3, project_index)
        create_project_page('test page 3', 'test', 'test', 4, project_index)
        create_project_page('test page 4', 'test', 'test', 5, project_index)

        res = ProjectPage.get_latest()
        self.assertEqual(res.count(), 3)
