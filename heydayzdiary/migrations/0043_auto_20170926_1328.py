# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heydayzdiary', '0042_auto_20170926_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day_entry_location',
            name='travel_distance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='day_entry_location',
            name='travel_time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]