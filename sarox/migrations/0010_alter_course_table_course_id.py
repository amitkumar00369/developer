# Generated by Django 5.0.2 on 2024-04-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0009_alter_course_table_course_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course_table",
            name="course_id",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]