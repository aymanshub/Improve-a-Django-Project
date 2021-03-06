# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-10-31 08:47
from __future__ import unicode_literals

from django.db import migrations
from datetime import date


def update_dates(apps, schema_editor):
    # We can't import the Menu model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    print("********DATA MIGRATION***********start")
    Menu = apps.get_model('menu', 'Menu')
    print("********One step before the loop")
    for menu in Menu.objects.all():
        print("working on menu {}".format(menu.id))
        print("created_date is: {}".format(menu.created_date))
        dt = menu.created_datetime
        menu.created_date = date(dt.year, dt.month, dt.day)
        dt = menu.expiration_datetime
        menu.expiration_date = date(dt.year, dt.month, dt.day) if dt else None
        menu.save()

    Item = apps.get_model('menu', 'Item')
    for item in Item.objects.all():
        dt = item.created_datetime
        item.created_date = date(dt.year, dt.month, dt.day)
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20191031_1045'),
    ]

    operations = [
        migrations.RunPython(update_dates),
    ]
