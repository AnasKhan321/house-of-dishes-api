# Generated by Django 4.2.4 on 2023-11-11 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_dish_kitchen_equiments_ingredient_unit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='kitchen_equiments',
            new_name='kitchen_equipments',
        ),
    ]