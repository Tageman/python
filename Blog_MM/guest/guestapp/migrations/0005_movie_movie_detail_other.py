# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-17 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guestapp', '0004_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_detail_other',
            field=models.CharField(default='bbb', max_length=1000),
        ),
    ]
