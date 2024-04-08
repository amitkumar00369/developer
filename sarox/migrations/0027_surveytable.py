# Generated by Django 5.0.2 on 2024-04-08 05:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0026_alter_course_table_course_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="SurveyTable",
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
                ("organisation_name", models.CharField(max_length=128)),
                (
                    "start_survey_date",
                    models.DateField(blank=True, default=django.utils.timezone.now),
                ),
                ("survey_type", models.CharField(blank=True, max_length=128)),
                ("survey_name", models.CharField(max_length=128)),
                ("Max_no_of_participants", models.BigIntegerField(blank=True)),
                ("language", models.CharField(max_length=128)),
                ("survey_questions", models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
