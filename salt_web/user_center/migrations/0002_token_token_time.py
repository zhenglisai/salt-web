# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-30 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='token_time',
            field=models.IntegerField(default=0),
        ),
    ]
