# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 08:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_projectindexpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectpage',
            name='name',
        ),
    ]
