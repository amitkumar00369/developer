# Generated by Django 5.0.2 on 2024-04-22 07:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sarox", "0040_allprogramtable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="allprogramtable",
            name="PPT",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="allprogramtable",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
