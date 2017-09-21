# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 11:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('heydayzdiary', '0004_auto_20170824_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='day_entry',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='day_entry',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
    ]
