# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 18:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_processed', '0019_auto_20161018_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatescrapedelection',
            name='type',
        ),
        migrations.RemoveField(
            model_name='propositionscrapedelection',
            name='type',
        ),
    ]