# Generated by Django 2.1.3 on 2018-11-28 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxcalc', '0002_auto_20181121_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxcalcinputs',
            name='quick_calc',
        ),
    ]
