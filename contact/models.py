from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField


class FormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', related_name='form_fields')


class ContactFormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname='full'),
        InlinePanel('form_fields', label='Formularfelder'),
        FieldPanel('thank_you_text', classname='full'),
        MultiFieldPanel([
            FieldPanel('to_address', classname='full'),
            FieldPanel('from_address', classname='full'),
            FieldPanel('subject', classname='full'),
        ], 'Email')
    ]
