# Generated by Django 3.0.10 on 2020-09-11 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0019_auto_20200906_1819"),
    ]

    operations = [
        migrations.RemoveField(model_name="deployment", name="tag_deprecated",),
        migrations.RemoveField(model_name="project", name="latest_tag_deprecated",),
        migrations.RemoveField(model_name="project", name="staging_tag_deprecated",),
    ]
