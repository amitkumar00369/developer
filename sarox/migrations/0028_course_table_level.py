# Generated by Django 5.0.2 on 2024-04-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0027_surveytable"),
    ]

    operations = [
        migrations.AddField(
            model_name="course_table",
            name="level",
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
