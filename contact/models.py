from wagtail.wagtailcore.models import Page

from django.db import models
from django.utils import timezone, text

from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField


class FormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', related_name='form_fields')


class ContactFormPage(AbstractEmailForm):
    intro = models.CharField(max_length=300, default='')
    thank_you_head = models.CharField(max_length=50, default='')
    thank_you_text = models.CharField(max_length=300, default='')

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname='full'),
        InlinePanel('form_fields', label='Formularfelder'),
        FieldPanel('thank_you_head', classname='full'),
        FieldPanel('thank_you_text', classname='full'),
        MultiFieldPanel([
            FieldPanel('to_address', classname='full'),
            FieldPanel('from_address', classname='full'),
            FieldPanel('subject', classname='full'),
        ], 'Email')
    ]

    def create_test(title, intro, parent=None):
        if (parent is None):
            parent = Page.get_first_root_node()
        contact = ContactFormPage(title=title, intro=intro, thank_you_head='f',
                                  thank_you_text='f', slug=text.slugify(title))
        parent.add_child(instance=contact)
        return contact
