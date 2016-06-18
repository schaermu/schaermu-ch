from django.test import TestCase

from .models import HomePage
from projects.models import ProjectPage, ProjectIndexPage


class HomePageTests(TestCase):
    def test_home_no_latest_projects(self):
        hpage = HomePage.create_test('Home Test', 'Leadtest')
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context['latest_projects'],
            []
        )

    def test_home_with_latest_projects(self):
        proj_idx = ProjectIndexPage.create_test('project index', 'test')
        ProjectPage.create_test('Project 1', 'test', 1, proj_idx)
        ProjectPage.create_test('Project 2', 'test', 1, proj_idx)

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context['latest_projects'],
            ['<ProjectPage: Project 1>', '<ProjectPage: Project 2>']
        )
