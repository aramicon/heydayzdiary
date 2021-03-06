# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heydayzdiary', '0023_work'),
    ]

    operations = [
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('description', models.TextField(blank=True)),
                ('day_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heydayzdiary.Day_entry')),
            ],
        ),
    ]
