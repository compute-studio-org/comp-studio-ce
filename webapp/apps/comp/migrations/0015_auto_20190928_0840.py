# Generated by Django 2.2.5 on 2019-09-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("comp", "0014_auto_20190805_1601")]

    operations = [
        migrations.AlterField(
            model_name="inputs",
            name="traceback",
            field=models.CharField(
                blank=True, default=None, max_length=8000, null=True
            ),
        ),
        migrations.AlterField(
            model_name="simulation",
            name="traceback",
            field=models.CharField(
                blank=True, default=None, max_length=8000, null=True
            ),
        ),
    ]