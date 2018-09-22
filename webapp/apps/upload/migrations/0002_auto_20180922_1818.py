# Generated by Django 2.1 on 2018-09-22 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('upload', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileoutput',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Profile'),
        ),
        migrations.AddField(
            model_name='fileoutput',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Project'),
        ),
    ]
