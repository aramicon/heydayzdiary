# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heydayzdiary', '0002_auto_20170821_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='day_entry',
            name='day_main_text',
            field=models.CharField(default='', max_length=10000),
            preserve_default=False,
        ),
    ]
