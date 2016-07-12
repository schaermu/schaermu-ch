#!/bin/bash
DJANGO_SETTINGS_MODULE=schaermu_ch.settings.dev django-admin.py dumpdata --natural-foreign --indent=2 -e contenttypes -e auth.Permission -e sessions -e wagtailcore.pagerevision > export.json
