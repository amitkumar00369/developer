# Generated by Django 5.0.2 on 2024-04-03 20:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0011_coursetable1"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coursetable1",
            old_name="id",
            new_name="courseid",
        ),
        migrations.RemoveField(
            model_name="coursetable1",
            name="course_id",
        ),
    ]