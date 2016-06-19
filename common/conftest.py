import pytest


@pytest.fixture(scope='class')
def site_structure(request):
    """
    Creates a basic site structure in wagtail to enable tests against
    a real site.
    """
    from wagtail.wagtailcore.models import Site

    from home.models import HomePage
    from projects.models import ProjectIndexPage
    from contact.models import ContactFormPage

    hpage = HomePage.create_test('Home Test', 'Leadtest')
    pIndex = ProjectIndexPage.create_test('Projekt Index', 'Lead', hpage)
    cIndex = ContactFormPage.create_test('Contact Form', 'Lead', hpage)

    site = Site.objects.create(hostname='foo.bar.test', root_page=hpage)
    if request.cls is not None:
        request.cls.site = site
        request.cls.home = hpage
        request.cls.projects = pIndex
        request.cls.contact = cIndex

    return site
