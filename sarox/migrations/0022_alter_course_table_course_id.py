# Generated by Django 5.0.2 on 2024-04-06 02:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0021_alter_course_table_course_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course_table",
            name="course_id",
            field=models.IntegerField(default=1),
        ),
    ]