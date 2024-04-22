# Generated by Django 5.0.2 on 2024-04-22 06:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0039_addthoughts_time_videotable_time"),
    ]

    operations = [
        migrations.CreateModel(
            name="allProgramTable",
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
                ("title", models.TextField(max_length=256, null=True)),
                ("video", models.FileField(blank=True, null=True, upload_to="videos/")),
                ("PPT", models.FileField(blank=True, null=True, upload_to="pdf/")),
                (
                    "date",
                    models.DateField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "time",
                    models.TimeField(blank=True, default=django.utils.timezone.now),
                ),
            ],
        ),
    ]
