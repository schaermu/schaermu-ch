from django.test import TestCase
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test.client import RequestFactory

from htmlmin.minify import html_minify

import pytest
import pprint


@pytest.mark.usefixtures('site_structure')
class CommonTests(TestCase):
    def render_tpl(self, template, context):
        t = Template(template)
        c = Context(context)
        return html_minify(t.render(c))

    def test_menu_items_generates_nav(self):
        req = self.client.get('/')
        req.site = self.site

        template = "{% load common_tags %}{% menu_items \
            parent=hpage calling_page=self %}"
        output = '<html><head></head><body><li class=""> \
            <a href="/projekt-index/">/ projekt index</a></li> \
            <li class=""><a href="/contact-form/">/ contact form</a></li> \
            </body></html>'
        res = self.render_tpl(template, {'hpage': self.home, 'request': req})

        self.assertHTMLEqual(output, res)

    def test_menu_items_flags_active_item(self):
        req = self.client.get('/projekt-index')
        req.site = self.site

        template = "{% load common_tags %}{% menu_items \
            parent=hpage calling_page=target_page %}"
        output = '<html><head></head><body><li class="active"> \
            <a href="/projekt-index/">/ projekt index</a></li> \
            <li class=""><a href="/contact-form/">/ contact form</a></li> \
            </body></html>'
        res = self.render_tpl(template, {'hpage': self.home,
                              'target_page': self.projects, 'request': req})

        self.assertHTMLEqual(output, res)
