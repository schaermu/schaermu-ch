from wagtail.tests.utils import WagtailPageTests

from home.models import *
from projects.models import *
from contact.models import *


class SiteStructureTests(WagtailPageTests):
    def test_check_homepage_constraints(self):
        self.assertAllowedSubpageTypes(HomePage, {ProjectIndexPage,
                                       ContactFormPage})

    def test_can_create_project_index(self):
        self.assertCanCreateAt(HomePage, ProjectIndexPage)
        self.assertAllowedSubpageTypes(ProjectIndexPage, {ProjectPage})

    def test_can_create_project(self):
        self.assertCanCreateAt(ProjectIndexPage, ProjectPage)
        self.assertCanNotCreateAt(HomePage, ProjectPage)
        self.assertAllowedSubpageTypes(ProjectPage, {})

    def test_can_create_contact(self):
        self.assertCanCreateAt(HomePage, ContactFormPage)
        self.assertAllowedSubpageTypes(ProjectPage, {})
