# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heydayzdiary', '0003_day_entry_day_main_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='question',
            new_name='day_entry',
        ),
    ]
