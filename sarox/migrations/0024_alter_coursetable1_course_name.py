# Generated by Django 5.0.2 on 2024-04-06 02:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0023_alter_coursetable1_course_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursetable1",
            name="course_name",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
