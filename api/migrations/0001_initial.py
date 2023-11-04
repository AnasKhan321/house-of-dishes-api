

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0002_chefuser"),
    ]

    operations = [
        migrations.CreateModel(

            name="Dish",
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
                ("name", models.CharField(max_length=100)),
                (
                    "veg_non_veg",
                    models.CharField(
                        choices=[("Veg", "Vegetarian"), ("NonVeg", "Non-Vegetarian")],
                        default="Veg",
                        max_length=7,
                    ),
                ),
                ("popularity_state", models.CharField(blank=True, max_length=100)),
                ("cuisine", models.CharField(blank=True, max_length=100)),
                (
                    "course_type",
                    models.CharField(
                        choices=[
                            ("MainCourse", "Main Course"),
                            ("Starter", "Starter"),
                            ("Dessert", "Dessert"),
                        ],
                        default="MainCourse",
                        max_length=12,
                    ),
                ),
                ("customizable_ingredients", models.BooleanField(default=False)),
                (
                    "cooking_time",
                    models.CharField(blank=True, default=None, max_length=10),
                ),
                (
                    "dish_picture",
                    models.ImageField(blank=True, null=True, upload_to="dish_images/"),
                ),
                (
                    "chef",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dish_set",
                        to="users.chefuser",
                    ),
                ),
            ],
        ),
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
        migrations.CreateModel(
            name="Instructions",
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
                ("step", models.CharField(max_length=200)),
                ("instruction_video_url", models.CharField(blank=True, max_length=500)),
                (
                    "dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="instructions",
                        to="api.dish",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ingredient",
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
                ("name", models.CharField(max_length=100)),
                ("quantity", models.IntegerField()),
                (
                    "dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredients",
                        to="api.dish",
                    ),
                ),

            ],
        ),
    ]
