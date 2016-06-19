from django.test import TestCase
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test.client import RequestFactory

from wagtail.wagtailcore.models import Site

from htmlmin.minify import html_minify

from home.models import HomePage
from projects.models import ProjectIndexPage
from contact.models import ContactFormPage


class CommonTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_menu_items_generates_nav(self):
        hpage = HomePage.create_test('Home Test', 'Leadtest')
        site = Site.objects.create(hostname='foo.bar.test',
                                   root_page=hpage)
        pIndex = ProjectIndexPage.create_test('Projekt Index', 'Lead', hpage)
        cIndex = ContactFormPage.create_test('Contact Form', 'Lead', hpage)
        req = self.factory.get('/')
        req.site = site

        template = "{% load common_tags %}{% menu_items \
            parent=hpage calling_page=self %}"
        t = Template(template)
        c = Context({'hpage': hpage, 'request': req})

        output = '<html><head></head><body><li class=""> \
            <a href="/projekt-index/">/ projekt index</a></li> \
            <li class=""><a href="/contact-form/">/ contact form</a></li> \
            </body></html>'
        self.maxDiff = None
        self.assertHTMLEqual(output, html_minify(t.render(c)))
