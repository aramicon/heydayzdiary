# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heydayzdiary', '0034_auto_20170921_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='web_tracking_system_url',
            field=models.URLField(blank=True),
        ),
    ]