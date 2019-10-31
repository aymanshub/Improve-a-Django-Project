# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-10-31 08:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20191031_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='menu',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]