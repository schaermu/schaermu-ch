from django.test import TestCase

from .models import ProjectPage, ProjectIndexPage


class ProjectPageTests(TestCase):
    def test_get_latest_returns_latest_projects(self):
        project_index = ProjectIndexPage.create_test('test index', 'test')
        ProjectPage.create_test('test page 1', 'test', 2, project_index)
        ProjectPage.create_test('test page 2', 'test', 3, project_index)
        ProjectPage.create_test('test page 3', 'test', 4, project_index)
        ProjectPage.create_test('test page 4', 'test', 5, project_index)

        res = ProjectPage.get_latest()
        self.assertEqual(res.count(), 4)
