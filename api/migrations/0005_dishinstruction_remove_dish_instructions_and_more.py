# Generated by Django 4.2.4 on 2023-09-13 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_dish_dish_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="DishInstruction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("instruction_text", models.TextField()),
                ("time_required", models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name="dish",
            name="instructions",
        ),
        migrations.AddField(
            model_name="dish",
            name="instructions",
            field=models.ManyToManyField(related_name="dish", to="api.dishinstruction"),
        ),
    ]
