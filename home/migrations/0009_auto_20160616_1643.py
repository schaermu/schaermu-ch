# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 16:43
from __future__ import unicode_literals

from django.db import migrations
import home.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_homepage_portrait_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title', label='Titel')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(label='Absatz')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('career', wagtail.wagtailcore.blocks.ListBlock(home.models.CareerItemBlock, icon='user', label='Karriere', template='blocks/career.html')), ('skills', wagtail.wagtailcore.blocks.ListBlock(home.models.CareerItemBlock, icon='pick', label='Skills', template='blocks/skills.html')))),
        ),
    ]
