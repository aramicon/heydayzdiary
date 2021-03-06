# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 13:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('heydayzdiary', '0043_auto_20170926_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='day_entry_location',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='day_entry_location',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exercise',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='location',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='meal',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meal',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='study',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='study',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='study_subject',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='study_subject',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='work',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default='2017-09-26', verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='work',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
        migrations.AddField(
            model_name='work',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='heydayzdiary.Job'),
        ),
    ]
