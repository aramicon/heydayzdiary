# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-26 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heydayzdiary', '0045_template_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='day_entry',
            name='is_template_day',
            field=models.BooleanField(default=False),
        ),
    ]
