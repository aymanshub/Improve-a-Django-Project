from django.db import migrations
from django.utils import timezone
from datetime import date


def update_dates(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    print("********DATA MIGRATION***********start")
    Menu = apps.get_model('menu', 'Menu')
    print("********One step before the loop")
    for menu in Menu.objects.all():
        print("working on menu {}".format(menu.id))
        # if not menu.created_date:
        #     menu.created_date = timezone.now().date()
        print("created_date is: {}".format(menu.created_date))
        dt = menu.created_date
        menu.created_date = date(dt.year, dt.month, dt.day)
        menu.save()


    # Item = apps.get_model('menu', 'Item')
    # for item in Item.objects.all():
    #     item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20191027_2359'),
    ]

    operations = [
        migrations.RunPython(update_dates),
    ]
