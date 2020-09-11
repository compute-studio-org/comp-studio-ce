# Generated by Django 3.0.10 on 2020-09-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0018_auto_20200906_1719"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="tag",
            constraint=models.UniqueConstraint(
                fields=("project", "image_tag"), name="unique_project_tag"
            ),
        ),
    ]
